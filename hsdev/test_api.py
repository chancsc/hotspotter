from __future__ import division, print_function


def parse_arguments(defaultdb, usedbcache):
    from hscom import argparse2
    from hscom import params
    from hscom import helpers as util
    from hscom import fileio as io
    import sys
    args = argparse2.parse_arguments(defaultdb=defaultdb)
    # Parse arguments
    args = argparse2.fix_args_with_cache(args)
    # fix args shortnam
    if (args.dbdir is None) and (args.db is not None):
        try:
            args.dbdir = params.dev_databases[args.db]
        except KeyError:
            pass
    # Lookup shortname
    try:
        inverse_dev_databases = params.inverse_dev_databases()
        args.db = inverse_dev_databases[args.dbdir]
    except KeyError:
        pass
    if usedbcache:
        if args.vdd:
            util.vd(args.dbdir)
            args.vdd = False
        if util.inIPython() or '--cmd' in sys.argv:
            args.nosteal = True
    params.args = args
    # Preload process args
    if args.delete_global:
        io.delete_global_cache()
    return args


def main(defaultdb='cache', preload=False, app=None):
    from hscom import fileio as io
    from hscom import params
    from hotspotter import HotSpotterAPI as api
    if app is True:
        from hsgui import guitools
        app, is_root = guitools.init_qtapp()
    args = parse_arguments(defaultdb, defaultdb == 'cache')
    # --- Build HotSpotter API ---
    if app is None:
        hs = api.HotSpotter(args)
    else:
        from hsgui import guiback
        back = guiback.make_main_window(app)
        hs = back.open_database(args.dbdir)
    setcfg = args.setcfg
    if setcfg is not None:
        import experiment_harness
        print('[main] setting cfg to %r' % setcfg)
        varied_list = experiment_harness.get_varied_params_list([setcfg])
        cfg_dict = varied_list[0]
        hs.prefs.query_cfg.update_cfg(**cfg_dict)
        hs.prefs.save()
        hs.prefs.printme()
    # Load all data if needed now, otherwise be lazy
    try:
        load_all = preload
        hs.load(load_all=load_all)
        db_dir = hs.dirs.db_dir
        io.global_cache_write('db_dir', db_dir)
    except ValueError as ex:
        print('[main] ValueError = %r' % (ex,))
        if params.args.strict:
            raise
    if app is not None:
        return hs, back
    else:
        from hsgui import guitools
        app, is_root = guitools.init_qtapp()
        hs.app = app
    return hs


def get_test_cxs(hs, max_testcases=None):
    valid_cxs = get_qcx_list(hs)
    if max_testcases is not None:
        max_ = max(max_testcases, len(valid_cxs) - 1)
        if max_ == 0:
            raise ValueError('[test_api] Database does not have test cxs')
        valid_cxs = valid_cxs[0:max_]
    return valid_cxs


def get_qcx_list(hs):
    ''' Function for getting the list of queries to test '''
    import numpy as np
    from hscom import params
    from hscom import helpers as util
    print('[dev] get_qcx_list()')

    def get_cases(hs, with_hard=True, with_gt=True, with_nogt=True, with_notes=False):
        qcx_list = []
        valid_cxs = hs.get_valid_cxs()
        if with_hard:
            if 'hard' in hs.tables.prop_dict:
                for cx in iter(valid_cxs):
                    if hs.cx2_property(cx, 'hard') == 'True':
                        qcx_list += [cx]
        if with_hard:
            if 'Notes' in hs.tables.prop_dict:
                for cx in iter(valid_cxs):
                    if hs.cx2_property(cx, 'Notes') != '':
                        qcx_list += [cx]
        if with_gt and not with_nogt:
            for cx in iter(valid_cxs):
                gt_cxs = hs.get_other_indexed_cxs(cx)
                if len(gt_cxs) > 0:
                    qcx_list += [cx]
        if with_gt and with_nogt:
            qcx_list = valid_cxs
        return qcx_list

    # Sample a large pool of query indexes
    histids = None if params.args.histid is None else np.array(params.args.histid)
    if params.args.all_cases:
        print('[dev] all cases')
        qcx_all = get_cases(hs, with_gt=True, with_nogt=True)
    elif params.args.all_gt_cases:
        print('[dev] all gt cases')
        qcx_all = get_cases(hs, with_hard=True, with_gt=True, with_nogt=False)
    elif params.args.qcid is None:
        print('[dev] did not select cases')
        qcx_all = get_cases(hs, with_hard=True, with_gt=False, with_nogt=False)
    else:
        print('[dev] Chosen qcid=%r' % params.args.qcid)
        qcx_all =  util.ensure_iterable(hs.cid2_cx(params.args.qcid))
    # Filter only the ones you want from the large pool
    if histids is None:
        qcx_list = qcx_all
    else:
        histids = util.ensure_iterable(histids)
        print('[dev] Chosen histids=%r' % histids)
        qcx_list = [qcx_list[id_] for id_ in histids]

    if len(qcx_list) == 0:
        if params.args.strict:
            raise Exception('no qcx_list history')
        qcx_list = [0]
    print('[dev] len(qcx_list) = %d' % len(qcx_list))
    qcx_list = util.unique_keep_order(qcx_list)
    return qcx_list


def reload_all():
    import dev_reload
    dev_reload.rrr()
    dev_reload.reload_all_modules()

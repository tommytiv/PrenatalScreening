
# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)





def report_CEA_CBA(simOutputs_none, simOutputs_anticoag):
    no_cvs_strategy=Econ.Strategy(name="No Diagnostic test", cost_obs=simOutputs_none.get_costs(),
                                      effect_obs=simOutputs_none.get_utilities())
    cvs_strategy=Econ.Strategy(name="Diagnostic Test", cost_obs=simOutputs_anticoag.get_costs(),
                                            effect_obs=simOutputs_anticoag.get_utilities())

    listofStrategies = [no_therapy_strategy, anticoag_therapy_strategy]

    CEA = Econ. CEA(listofStrategies, if_paired=False)

    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

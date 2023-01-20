from policyengine_canada.model_api import *


class on_child_care_fee_subsidy_reduction(Variable):
    value_type = float
    entity = Person
    label = "Ontario Child Care Fee Subsidy reduction"
    unit = CAD
    definition_period = YEAR

    def formula(person, period, parameters):
        children = person("on_child_care_fee_subsidy_children", period)
        eligible_children = person(
            "on_child_care_fee_subsidy_reduction_children", period
        )
        full_time = person("full_time_childcare", period)
        reduction_factor = parameters(
            period
        ).gov.provinces.on.subsidies.on_child_care_fee_subsidy.reduction.factor
        full_factor = eligible_children * reduction_factor / children
        full_time_reduction = person(
            "on_child_care_fee_subsidy_full_time", period
        )
        part_time_reduction = person(
            "on_child_care_fee_subsidy_part_time", period
        )
        eligible = children > 0
        return (
            eligible
            * full_factor
            * where(full_time, full_time_reduction, part_time_reduction)
        )

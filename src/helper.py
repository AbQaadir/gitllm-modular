def format_plans(plans):
    formatted_text = ""

    for plan in plans:
        # Extract the plan description and tool parameters
        plan_description = plan.plan
        tool_name = plan.tool
        tool_params = plan.tool_params
        e_number = plan.e_number

        # Format the plan and tool invocation
        formatted_text += f"Plan: {plan_description}\n"
        formatted_text += f"#E{e_number} = {tool_name}[{tool_params}]\n\n"

    return formatted_text.strip()




def create_tuples_from_plans(plans):
    tuples_list = []

    for plan in plans:
        # Extract the relevant attributes
        plan_description = plan.plan
        e_number = f"#E{plan.e_number}"
        tool_name = plan.tool
        tool_params = plan.tool_params

        # Create a tuple with the extracted values
        plan_tuple = (plan_description, e_number, tool_name, tool_params)

        # Add the tuple to the list
        tuples_list.append(plan_tuple)

    return tuples_list



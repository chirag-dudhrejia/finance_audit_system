def critic(state):
    category = state.get("category")

    valid = category is not None and len(category) > 2

    return {**state, "valid": valid}
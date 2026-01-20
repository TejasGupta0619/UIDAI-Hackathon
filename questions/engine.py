def answer_question(question_id, df, **params):
    if question_id not in QUESTION_REGISTRY:
        raise ValueError(f"Unknown question: {question_id}")

    q = QUESTION_REGISTRY[question_id]
    result = q["compute"](df, **params)

    return {
        "question_id": question_id,
        "type": q["type"],
        "description": q["description"],
        "metrics_used": q["metrics"],
        "params": params,
        "result": result.reset_index().to_dict(orient="records")
    }

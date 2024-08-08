from decimal import Decimal

from bot.db.models import AIModel


def predict_generation_cost(ai_model: AIModel, input_tokens: int) -> Decimal:
    """Predict the cost of generating output using an AI model.

    This is an approximate prediction to help minimize requests from users with insufficient balance.
    """
    avg_output_tokens = input_tokens * 2.5
    total_tokens = input_tokens + avg_output_tokens
    return ai_model.price * Decimal(total_tokens)

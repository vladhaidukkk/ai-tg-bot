from decimal import Decimal

from bot.db.models import AIModel


def predict_text_generation_cost(ai_model: AIModel, input_tokens: int) -> Decimal:
    """Predict the cost of text generating output using an AI model.

    This is an approximate prediction to help minimize requests from users with insufficient balance.
    """
    avg_output_tokens = input_tokens * 2.5
    total_tokens = input_tokens + avg_output_tokens
    return ai_model.price * Decimal(total_tokens)


def predict_image_generation_cost(ai_model: AIModel, images_number: int = 1) -> Decimal:
    """Predict the cost of image generating output using an AI model.

    This is an approximate prediction to help minimize requests from users with insufficient balance.
    """
    return ai_model.price * Decimal(images_number)

"""
Gemma-2B-IT model implementation.

This module provides:
1. Hardware detection for MPS, CUDA, and CPU.
2. 4-bit model quantization using BitsAndBytes.
3. Conversational response generation using the model's chat template.
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)


MODEL_ID = "google/gemma-2b-it"


def detect_device():
    """Detect the best available computation device."""

    if torch.backends.mps.is_available():
        return "mps"

    if torch.cuda.is_available():
        return "cuda"

    return "cpu"


def load_model(model_id=MODEL_ID, use_quantization=True):
    """
    Load the Gemma model and its tokenizer.

    Args:
        model_id: Hugging Face model repository.
        use_quantization: Whether to enable 4-bit quantization.

    Returns:
        A tuple containing the model and tokenizer.
    """

    device = detect_device()
    print(f"Selected device: {device}")

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    compute_dtype = (
        torch.float32 if device == "cpu"
        else torch.float16
    )

    load_options = {
        "device_map": device,
        "dtype": compute_dtype,
    }

    if use_quantization:
        print("Configuring 4-bit quantization...")

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
        )

        load_options["quantization_config"] = quantization_config

    print(f"Loading model: {model_id}")

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            **load_options,
        )

    except Exception as error:
        raise RuntimeError(
            f"Failed to load model on {device}. "
            "Please check the model access, memory, "
            "and quantization backend."
        ) from error

    model.eval()

    print("Model loaded successfully!")
    print(f"Device: {device}")
    print(f"Quantized: {getattr(model, 'is_quantized', 'Unknown')}")

    return model, tokenizer


def get_response(
    prompt,
    model,
    tokenizer,
    max_length=150,
    temperature=0.7,
    top_p=0.9,
):
    """
    Generate a response from the loaded language model.

    Args:
        prompt: User's input text.
        model: Loaded language model.
        tokenizer: Model tokenizer.
        max_length: Maximum number of new tokens.
        temperature: Sampling temperature. Use 0 for deterministic output.
        top_p: Nucleus sampling probability.

    Returns:
        The generated assistant response as a string.
    """

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")

    if max_length <= 0:
        raise ValueError("max_length must be greater than zero.")

    if temperature < 0:
        raise ValueError("temperature cannot be negative.")

    if not 0 < top_p <= 1:
        raise ValueError("top_p must be greater than 0 and at most 1.")

    # Construct the conversation.
    conversation = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    # Apply the model's native chat template.
    inputs = tokenizer.apply_chat_template(
        conversation,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    # Place input tensors on the same device as the model.
    input_device = model.device

    inputs = {
        name: tensor.to(input_device)
        for name, tensor in inputs.items()
    }

    prompt_length = inputs["input_ids"].shape[-1]

    # Configure text generation.
    generation_options = {
        "max_new_tokens": max_length,
        "do_sample": temperature > 0,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
    }

    if temperature > 0:
        generation_options["temperature"] = temperature
        generation_options["top_p"] = top_p

    # Generate the assistant's response.
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            **generation_options,
        )

    # Extract newly generated tokens only.
    generated_tokens = output_ids[0, prompt_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    return response.strip()
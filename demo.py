"""
Interactive terminal application for Gemma-2B-IT.
"""

from src.model import load_model, get_response


def main():
    print("=" * 55)
    print("       GEMMA-2B-IT INTERACTIVE CHAT")
    print("=" * 55)

    print("\nInitializing model...")

    try:
        model, tokenizer = load_model()
    except Exception as error:
        print(f"\n[ERROR] Model initialization failed: {error}")
        raise SystemExit(1)

    print("\nModel is ready!")
    print("Enter 'quit' or 'exit' to stop.")
    print("-" * 55)

    while True:
        try:
            user_input = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            break

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            response = get_response(
                prompt=user_input,
                model=model,
                tokenizer=tokenizer,
                max_length=128,
                temperature=0.7,
                top_p=0.9,
            )

            print(f"\nGemma: {response}")

        except Exception as error:
            print(f"\n[ERROR] Response generation failed: {error}")


if __name__ == "__main__":
    main()

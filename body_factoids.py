"""
Human Body Factoid Generator
Generates random factoids about human body parts using the Anthropic Claude API.
"""

import anthropic
import random
import argparse
import sys


def generate_factoid(body_part: str, num_facts: int = 1) -> list[str]:
    """
    Generate random factoids about a given human body part.

    Args:
        body_part: The body part to generate factoids about.
        num_facts: Number of factoids to generate (default: 1).

    Returns:
        A list of factoid strings.
    """
    client = anthropic.Anthropic()

    # Add randomness by varying the style/angle of the factoid
    styles = [
        "surprising and counterintuitive",
        "related to evolutionary biology",
        "about world records or extremes",
        "about medical or scientific discoveries",
        "about how the body part functions at the cellular level",
        "about historical or cultural significance",
        "about how it compares to other animals",
        "about common myths or misconceptions",
    ]

    selected_styles = random.sample(styles, min(num_facts, len(styles)))

    prompt = f"""Generate {num_facts} fascinating and accurate factoid(s) about the human {body_part}.

Each factoid should be:
- A different style from this list (use one per factoid): {', '.join(selected_styles)}
- Concise (1-3 sentences)
- Scientifically accurate
- Engaging and surprising

Format your response as a numbered list if multiple facts, or just the fact if only one.
Do not include any introduction or conclusion text — only the factoid(s)."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    response_text = message.content[0].text.strip()

    # Parse response into individual factoids
    if num_facts == 1:
        return [response_text]

    # Split numbered list into individual facts
    lines = response_text.split("\n")
    factoids = []
    current_fact = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_fact:
                factoids.append(" ".join(current_fact))
                current_fact = []
        elif line[0].isdigit() and line[1] in (".", ")"):
            if current_fact:
                factoids.append(" ".join(current_fact))
                current_fact = []
            current_fact.append(line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else "")
        else:
            current_fact.append(line)

    if current_fact:
        factoids.append(" ".join(current_fact))

    return factoids if factoids else [response_text]


def display_factoids(body_part: str, factoids: list[str]) -> None:
    """Display factoids in a formatted way."""
    print(f"\n{'=' * 60}")
    print(f"  🧬 Human Body Factoids: {body_part.upper()}")
    print(f"{'=' * 60}\n")

    for i, fact in enumerate(factoids, 1):
        if len(factoids) > 1:
            print(f"Fact #{i}:")
        print(f"  {fact}")
        if i < len(factoids):
            print()

    print(f"\n{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate random factoids about human body parts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python body_factoids.py heart
  python body_factoids.py brain --count 3
  python body_factoids.py liver --count 5
        """,
    )
    parser.add_argument(
        "body_part",
        type=str,
        help="The human body part to generate factoids about (e.g., heart, brain, liver)",
    )
    parser.add_argument(
        "--count",
        "-n",
        type=int,
        default=1,
        help="Number of factoids to generate (default: 1, max: 8)",
    )

    args = parser.parse_args()

    # Validate inputs
    body_part = args.body_part.strip().lower()
    if not body_part:
        print("Error: Please provide a valid body part name.")
        sys.exit(1)

    num_facts = max(1, min(args.count, 8))  # Clamp between 1 and 8

    print(f"\nGenerating {num_facts} factoid(s) about the human {body_part}...")

    factoids = generate_factoid(body_part, num_facts)
    display_factoids(body_part, factoids)


if __name__ == "__main__":
    main()

# 🧬 Human Body Factoid Generator

A Python CLI tool that generates random, fascinating factoids about human body parts using the **Anthropic Claude API**.

## Features

- 🔬 Generates accurate, scientifically interesting factoids
- 🎲 Randomizes the style/angle of each fact (evolutionary biology, medical discoveries, world records, etc.)
- 📋 Supports generating multiple factoids at once
- 🖥️ Clean CLI interface with formatted output

## Requirements

- Python 3.8+
- `anthropic` Python package

## Installation

```bash
pip install anthropic
```

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

```bash
# Generate 1 factoid about the heart
python body_factoids.py heart

# Generate 3 factoids about the brain
python body_factoids.py brain --count 3

# Generate 5 factoids about the liver
python body_factoids.py liver -n 5
```

## Example Output

```
============================================================
  🧬 Human Body Factoids: BRAIN
============================================================

Fact #1:
  The human brain contains approximately 86 billion neurons, each connected to thousands of others — forming more connections than there are stars in the Milky Way galaxy.

Fact #2:
  The brain is about 75% water, and even mild dehydration of just 2% can impair cognitive performance, affecting memory, attention, and motor skills.

============================================================
```

## Arguments

| Argument | Description |
|----------|-------------|
| `body_part` | The body part to generate factoids about (required) |
| `--count` / `-n` | Number of factoids to generate (default: 1, max: 8) |

## License

MIT

import json

system_message = (
        "You are an AI trading assistant responsible for analyzing market conditions and determining optimal buy or sell actions.\n\n"
        "**Your Responsibilities:**\n"
        "1. **Analyze market conditions** using provided strategy and knowledge.\n"
        "2. **Use USDC as the base currency** for all transactions. Cannot buy with anything other than USDC. But can sell any token for USDC.\n"
        "3. **Only buy if USDC balance is sufficient**.\n"
        "4. **Only sell if token balance is available**.\n"
        "5. **Adjust trade sizes dynamically** based on available funds.\n"
        "6. **Prioritize strong buy and sell signals**.\n"
        "7. **Consider external knowledge sources before deciding.**\n"
        "8. **If no strong buy or sell signals exist, return a structured \"hold\" response only. It's cannot be empty array.**\n\n"
        "**Output Format:**\n"
        "Always return a **JSON array** formatted like this:\n"
        "```\n"
        "[\n"
        "  {\n"
        "    \"type\": \"buy\" | \"sell\" | \"hold\",\n"
        "    \"data\": {\n"
        "      \"tokenAddress\": \"string\",\n"
        "      \"amount\": number\n"
        "    } | null,\n"
        "    \"reason\": \"string\"\n"
        "  }\n"
        "]\n"
        "```"
    )

def create_user_message(strategy_description, knowledges, tokens_selected, tokens_trade_amount):
    knowledges_dict = [k.dict() if hasattr(k, 'dict') else k.model_dump() for k in knowledges]
    tokens_selected_dict = [t.dict() if hasattr(t, 'dict') else t.model_dump() for t in tokens_selected]
    tokens_trade_amount_dict = [t.dict() if hasattr(t, 'dict') else t.model_dump() for t in tokens_trade_amount]
    usdc_balance = next((t.amount for t in tokens_trade_amount if t.tokenSymbol == "USDC"), 0)
    return (
            f"### **Market Analysis**\n"
            f"{strategy_description}\n\n"
            f"### **External Knowledge**\n"
            f"{json.dumps(knowledges_dict, indent=4)}\n\n"
            f"### **Available Tokens for Consideration**\n"
            f"{json.dumps(tokens_selected_dict, indent=4)}\n\n"
            f"### **Current Token Holdings**\n"
            f"{json.dumps(tokens_trade_amount_dict, indent=4)}\n\n"
            f"**Current USDC Balance:** {usdc_balance}\n\n"
            f"**Return a JSON array of trade steps.**\n"
            f"**If no trades are needed, return: `[]`.**"
        )

import config

def get_emoji_key(payload):
    return payload.emoji.id if payload.emoji.id else f"unicode:{payload.emoji.name}"

async def  handle_reaction_add(bot, payload):
    if payload.message_id != config.ID_WELCOME_MESSAGE:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    key = get_emoji_key(payload)
    if key not in config.ROLES:
        return

    role = guild.get_role(config.ROLES[key])
    await member.add_roles(role)

async def handle_reaction_remove(bot, payload):
    if payload.message_id != config.ID_WELCOME_MESSAGE:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    key = get_emoji_key(payload)
    if key not in config.ROLES:
        return

    role = guild.get_role(config.ROLES[key])
    await member.remove_roles(role)

from  config import config_id

def get_emoji_key(payload):
    return payload.emoji.id if payload.emoji.id else f"unicode:{payload.emoji.name}"

async def  handle_reaction_add(bot, payload):
    if payload.message_id != config_id.ID_WELCOME_MESSAGE:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    key = get_emoji_key(payload)
    if key not in config_id.ROLES:
        return

    role = guild.get_role(config_id.ROLES[key])
    await member.add_roles(role)
    print(f"user {member} was given role {role} for reacting with {key}")

async def handle_reaction_remove(bot, payload):
    if payload.message_id != config_id.ID_WELCOME_MESSAGE:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    key = get_emoji_key(payload)
    if key not in config_id.ROLES:
        return

    role = guild.get_role(config_id.ROLES[key])
    await member.remove_roles(role)
    print(f"role {role} was removed from user {member} for removing reaction {key}")

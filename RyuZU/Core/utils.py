def is_owner(bot, author):
    for owner in bot.config['owner_usernames']:
        p = owner.split("#")
        if p[0] == author.name and p[1] == author.discriminator:
            return True
    return False

import discord

version = "2.0.0"

client_id = 609563132523708426

intents = discord.Intents().all()

owners = [
  173237945149423619  # Kanin - Please keep my ID here
]

colors = {
    "main": 0xe67e22,
    "error": 0xe74c3c
}

prefixes = {
    "main": [
        "!"
    ],
    "debug": [
        "!!"
    ]
}

channels = {
  "fishing": 625642718860673044
}

time_format = "%A, %B %d %Y @ %I:%M%p %Z"

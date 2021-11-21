import random

async def chooseWinner(message):
  mes = message.content.split("~giveaway ", 1)[1]
  rolelist = []
  for i in range(0, len(mes), 18):
    rolelist.append(mes[i:i+18])
    break

  roleid = int(rolelist[0])
  server = message.channel.guild
  role = server.get_role(roleid)
  if role == None:
    await message.channel.send("Couldn't find that role")
  else:
    memberlist = []
    for member in server.members:
      if role in member.roles:
        memberlist.append(member.id)
    winner = int(random.choice(memberlist))
    await message.channel.send("<@{0}> is the winner!".format(winner))
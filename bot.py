import discord
import time
from discord.ext import commands

TOKEN = 'NTIyNzk4NTQwMzg1NDE5MjY0.DvQUsA.yQLRkvkc06KHNRoeu2bDeHzhpxY'
client = commands.Bot(command_prefix='$')
memberdict = {
    "Paulchen": "Maxi Schwanger",
    "MaxderHoden": "Björn Favorite Jeans",
    "Xiahou Dun": "Penner Jammerfrauer",
    "Kaomir": "Fabian Hammerbauer",
    "MP_134": "Julius Schlaghart",
    "billabo": "Nils Schneller",
    "Vino": "Marco Weingratis",
    "Garnele": "Chair ImMomentBesetzt",
    "Waffi": "Fred hartzIV",
    "Limi0": "Harry Reichthart",
    "jkk": "Dorian Lidl",
    "Dennis": "Denise Fusch",
    "CharlesTheB": "Charles Winnitu"
}
vote = 'f'
votecp = 0
voteuser = ''
countyes = 0


@client.command(pass_context=True)
async def helpme(ctx):
    await client.say(ctx.message.author.mention + ' lutscht Schwänze.')


@client.command(pass_context=True)
async def give(ctx, user: discord.Member, numcp=0):
    if user:
        p = '{}'.format(user.name)
        a = '{}'.format(ctx.message.author)
        if p in memberdict and numcp in range(-11, 11):
            await update_cp(memberdict[p], numcp, user)
            await update_log(a, p, numcp)
            if numcp > 0:
                await client.say(user.mention + ' bekam ' + str(numcp) + ' Social Credit Points gutgeschrieben.')
            else:
                await client.say(user.mention + ' bekam ' + str(numcp) + ' Social Credit Points abgezogen.')
        elif numcp not in range(-11, 11):
            await client.say('Error. Credits müssen im Bereich zwischen -10 und 10 liegen.')
        else:
            await client.say(user.mention + ' ist dem Social Credit System noch nicht bekannt.')


@client.command(pass_context=True)
async def score(ctx):
    with open(r'D:\Workspace\python-workspace\DiscordBot\cp\cp.txt', 'r') as cp_data:
        data = cp_data.read()
        await client.say(data)


@client.command(pass_context=True)
async def vote(ctx, user: discord.Member, numcp=0, reason=''):
    global vote, voteuser, votecp
    if user:
        if vote == "t":
            await client.say('Es findet bereits eine Abstimmung statt')
        else:
            vote = "t"
            voteuser = '{}'.format(user.name)
            votecp = numcp
            if numcp > 0:
                await client.say(user.mention + ' ' + str(numcp) + ' Social Credits hinzufügen? (Grund: ' + reason + ')')
            elif numcp < 0:
                await client.say(user.mention + ' ' + str(numcp) + ' Social Credits abziehen? (Grund: ' + reason + ')')


@client.command(pass_context=True)
async def j(ctx):
    global countyes, votecp, voteuser, vote
    if voteuser == '':
        await client.say('Es ist keine Abstimmung am laufen.')
    else:
        votes = []
        if ctx.message.author.name not in votes:
            votes.append(ctx.message.author.name)
            countyes += 1
            if countyes >= 1:
                await client.say('Abstimmung erfolgreich.')
                await update_cp(memberdict[voteuser], votecp, None)
                vote = "f"
                voteuser = ''
                votecp = 0
                countyes = 0


@client.command(pass_context=True)
async def endvote(ctx):
    global vote, voteuser, votecp, countyes
    vote = 'f'
    voteuser = ''
    votecp = 0
    countyes = 0
    await client.say("Die Abstimmung wurde abgebrochen.")


async def update_cp(person, numcp, user):
    pointsold = 0
    cp_data = open(r'D:\Workspace\python-workspace\DiscordBot\cp\cp.txt', 'r')
    lines = cp_data.readlines()
    cp_data.close()

    cp_data = open(r'D:\Workspace\python-workspace\DiscordBot\cp\cp.txt', 'w')
    for index, line in enumerate(lines):
        if line.startswith(person):
            pointsold = int(line.split(':')[1])
            pointsnew = pointsold + numcp
            lines[index] = line.replace(str(pointsold), str(pointsnew))
            cp_data.write(lines[index])
        else:
            cp_data.write(line)
    cp_data.close()
    await update_name(user, numcp, pointsold)


async def update_name(user, newcp, oldcp):
    nick = user.display_name
    d = len(nick) - len(getrank(oldcp))
    rank = nick[d:]
    newrank = getrank(newcp)
    nicknorank = nick[:d]
    try:
        if not rank == newrank:
            newname = nicknorank + newrank
            await client.change_nickname(user, newname)
    except:
        pass


def getrank(cp):
    if cp < 0 and cp > -100:
        return '[Inder]'
    elif cp < -99 and cp > -200:
        return '[TS3]'
    elif cp < -199:
        return '[Schwanzlutscher]'
    elif cp > 0 and cp < 100:
        return '[egj]'
    elif cp > 99 and cp < 200:
        return '[Vorbild]'
    elif cp > 199:
        return '[Gottgleich]'
    else:
        return ''


async def update_log(author, victim, cp):
    logdate = time.strftime("%d.%m.%Y %H:%M:%S")
    log_data = open(r'D:\Workspace\python-workspace\DiscordBot\log\log.txt', 'a')
    logtext = "[" + logdate + "]" + "(" + author + ")" + ": $give " + memberdict[victim] + " " + str(cp) + "\n"
    log_data.write(logtext)
    log_data.close()


'''
@give.error
async def give_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await client.say('Error. Kein Servermitglied ausgewählt!')
'''


@client.event
async def on_ready():
    print('Ready')

client.run(TOKEN)

import discord
from discord.ext import commands
from config import *
import asyncio
from random import choice
from time import asctime, sleep

punished_users = {}
Client = discord.Client()
bot = commands.Bot(command_prefix='%', description=bot_description)



@bot.event
async def on_ready():
    print('>>Cock bot has connected to discord...')


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

        # Inside-channel functions
    if msg.author.id != bot_client_id and msg.channel.id == jail_channel_id:

        '''Cock-game check'''
        splited_message = msg.content.lower().split(' ')
        if 'петух' in splited_message and 'админ' in splited_message:
            await bot.send_message(msg.channel, choice(banana_phrases).format(msg.author.display_name))
            listed_users = open('listed_users.txt', 'r')
            listed_users_linelist = list(listed_users.readlines())
            listed_users.close()
            if msg.author.id + '\n' in listed_users_linelist:
                user_list_id = listed_users_linelist.index(msg.author.id + '\n')
                bananas = open('bananas_score.txt', 'r')
                current_scores = [score_line for score_line in bananas.readlines()]
                current_scores[user_list_id] = str(int(current_scores[user_list_id][:-1]) + 1) + '\n'
                bananas.close()
                bananas = open('bananas_score.txt', 'w')
                bananas.writelines(current_scores)
                bananas.close()
                print('{} threw 1 more banana! \t {}'.format(msg.author.display_name, asctime()))
                with open('bananas_score.txt', 'r'):
                    amount_of_bananas = int(bananas.readlines()[listed_users_linelist.index(msg.author.id + '\n')][:-1])
                    if amount_of_bananas == 500:
                        role = discord.utils.get(msg.server.roles, name='криминальный авторитет')
                        bot.add_roles(msg.author, role)
                        bot.send_message(msg.channel, 'Теперь {} {}!'.format(msg.author.display_name, role.name))
                    if amount_of_bananas == 5000:
                        role = discord.utils.get(msg.server.roles, name='кинг-конг')
                        bot.add_roles(msg.author, role)
                        bot.send_message(msg.channel, 'Теперь {} {}!'.format(msg.author.display_name, role.name))
            else:
                with open('listed_users.txt', 'a') as listed_users:
                    listed_users.write(msg.author.id + '\n')
                with open('bananas_score.txt', 'a') as bananas_score:
                    bananas_score.write('1\n')
                print('{} threw 1 more banana! \t {}'.format(msg.author.display_name, asctime()))

        '''score command'''
        if msg.content == '$score':
            listed_users = open('listed_users.txt', 'r')
            listed_users_linelist = list(listed_users.readlines())
            listed_users.close()
            if msg.author.id + '\n' in listed_users_linelist:
                with open('bananas_score.txt', 'r') as bananas_score:
                    amount_of_bananas = bananas_score.readlines()[listed_users_linelist.index(msg.author.id + '\n')]
                    last_int = int(amount_of_bananas[-2])
                    if last_int == 1:
                        ending = ''
                    elif 4 >= last_int <= 2:
                        ending = 'а'
                    else:
                        ending = 'ов'
                    await bot.send_message(
                        msg.channel, '{}, ты кинул {} банан{} в админа'.format(
                            msg.author.display_name, amount_of_bananas[:-1], ending
                        )
                    )
            else:
                await bot.send_message(msg.channel, 'Ты не кинул в админа ни одного банана!')

        # Non-channel functions
    if msg.author.id != bot_client_id and msg.channel.id != jail_channel_id:
        global prev_msg_content
        ''' Message length check'''
        if len(msg.content) > 40:
            await bot.send_message(msg.channel, choice(warning_message).format(msg.author.id))
            if msg.author.id in list(punished_users.keys()):
                punished_users[msg.author.id] += 1
                if punished_users[msg.author.id] >= 5:
                    role = discord.utils.get(msg.server.roles, name='криминальный авторитет')
                    jail_channel = discord.utils.get(msg.server.channels, name='обезьянник')
                    await bot.add_roles(msg.author, role)
                    await bot.move_member(msg.author, jail_channel)
            else:
                punished_users[msg.author.id] = 1
            sleep(3)
            await bot.delete_message(msg)
        ''' Repeatative content check'''
        if prev_msg_content == msg.content:
            await bot.delete_message(msg)
            print('> Deleted repeated content \t ' + asctime())
        else:
            prev_msg_content = msg.content


bot.run(bot_token)

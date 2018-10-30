#! /usr/bin/env python

import json
import os
import re
import sys
import time

import requests

if os.name == 'posix':
  import readline

def get_images(save_location, board, thread_num, categories):

  user_agent = {'User-agent': 'archive svc'}
  sess = requests.Session()
  sess.headers.update(user_agent)

  thread_url = f'http://a.4cdn.org/{board}/thread/{thread_num}.json'

  with sess.get(thread_url, ) as r:
    thread_json = r.text
    thread = r.json()

      # do req again

  images = [f"{p['tim']}{p['ext']}" for p in thread['posts'] if 'tim' in p]
  # print(images)
  # quit()

  
  for idx, image in enumerate(images):
    # print(post['tim'])

    # sleep a sec to follow da rulez
    time.sleep(1.1)

    image_url = f'http://i.4cdn.org/{board}/{image}'

    # download the images now:
    with sess.get(image_url) as i:
      # i.raw.decode_content = True
      # image_bin = i.raw
      image_bin = i.content
      # print(image_url)
      # print(i.text[:20])

    path = f'{save_location}/{thread_num}'

    if not os.path.exists(path):
      os.makedirs(path)

    with open(f'{path}/{thread_num}.json', 'w') as f:
      f.write(thread_json)

    with open(f'{path}/categories.txt', 'w') as f:
      f.write('\n'.join(categories))

    with open(f'{path}/{image}', 'wb') as f:
      # r.raw.decode_content = True
      f.write(image_bin)

    print(f'DONE {idx + 1} OUT OF {len(images)}')

def repl(save_location, board):

  def helpmsg():
  
    print('Type the number of the thread to grab followed by a comma-separated list of the tags for the thread. Type "help" to show this message. Type "quit" or "q" to quit')
    print('Example: 11111111 election interference, midterm bombings')
    print('Please watch your spelling. If you spell it wrong, just re-do it :)')

  helpmsg()

  while True:

    user_input = input(' > ')    

    if re.match(f'\d+', user_input):

      user_input = user_input.split(' ', 1)

      if len(user_input) > 1:
        thread, categories = user_input
      else:
        thread, categories = user_input[0], ''

      print(thread)
      print(categories)
      
      categories = [c.strip() for c in categories.split(',')]
      try:
        get_images(save_location, board, thread, categories)
      except json.decoder.JSONDecodeError:
        print("Check to ensure thread number is correct and that you are not blocked")
        print("To check if you're blocked, visit http://a.4cdn.org/boards.json and confirm the site does not perform a browser check.")
    elif user_input == 'q' or user_input == 'quit':
      confirm = input('Are you sure you want to quit? Y/n: ')
      if 'y' in confirm.lower():
        quit()
    else:
      helpmsg()
    

def parse_args(args):
  # positional args:
  # save location
  # board
  
  # optional position args:
  # thread_num. If repl is set, ignored, else required

  # flags
  # -r / --repl : pseudo repl. allow user to repeatedly grab threads

  if len(args) < 3:
    msg = """
    ARGUMENTS:
      4chan-thread-image-grabber.py <save location> <board> [<thread>|-r|--repl]

      save location: e.g. Y:4chan_stuff/midterm
      board: e.g. pol
      thread: e.g. 111111111

      -r | --repl : start in REPL mode to keep entering threads
    """
    print(msg)
    quit()

  parsed_args = dict()

  if '-r' in args or '--repl' in args:
    parsed_args['repl'] = True

    # in case someone did it with classic unix flags before positional args
    if '-r' in args:
      args.remove('-r')
    else:
      args.remove('--repl')
  else:
    # thread is required if repl not set
    parsed_args['thread'] = args[2]
    parsed_args['repl'] = False

  parsed_args['save'] = args[0]
  parsed_args['board'] = args[1]
  
  return parsed_args


def main(args):

  p_args = parse_args(args)

  if not p_args['repl']:
    get_images(p_args['save'], p_args['board'], p_args['thread'])
  else:
    repl(p_args['save'], p_args['board'])

if __name__ == '__main__':
  main(sys.argv[1:])
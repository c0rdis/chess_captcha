import urllib2
import re

baseurl = 'http://en.lichess.org/'

def simple_parse(text,start,end):
    pos1 = text.find(start)+len(start)
    pos2 = text.find(end, pos1)
    return text[pos1:pos2]

def submit_solution(captcha_id,solution):
    solution_url = baseurl+'captcha/'+captcha_id+'?solution='+solution
    return solution_url, urllib2.urlopen(solution_url).read()

def main():
    # getting captcha ID
    signup_url = baseurl+'signup'
    html = urllib2.urlopen(signup_url).read()    
    captcha_id = simple_parse(html,'<input type="hidden" name="gameId" id="gameId" value="','"')
    
    # obtaining moves
    captcha_url = baseurl+captcha_id
    captcha_solution = urllib2.urlopen(captcha_url).read()
    game = simple_parse(captcha_solution,'<div class="pgn">','is checkmated')
    game = simple_parse(game,'2.','# { ')
    moves = re.split('\d+\. ',game)
    
    #determining winning color, figure and last move
    color = 0
    last_move = moves[-1].split()
    if len(last_move) == 2:
        color = 1
    winner_move = last_move[-1]
    figure = winner_move[0]
    solution = winner_move[-2:]
    
    # finding last move for the specific color and figure
    for move in reversed(moves[:-1]):
        move = move.split()[color]
        if move[0] == figure:
            if move[-1] > '0' and move[-1] < '9':
                solution = move[-2:] + '+' + solution
            else:
                solution = move[-3:-1] + '+' + solution
            print submit_solution(captcha_id,solution)
            exit()
        
if __name__ == '__main__':
    main()

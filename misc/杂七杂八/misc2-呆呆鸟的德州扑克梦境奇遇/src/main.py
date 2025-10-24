import os
import random

flag = os.getenv('GZCTF_FLAG')

BANNER = r'''
                                                             ,----,            
,-.----.           ,--.                                    ,/   .`|            
\    /  \      ,--/  /|            .---.   ,----..       ,`   .'  :     ,---,. 
|   :    \  ,---,': / '           /. ./|  /   /   \    ;    ;     /   ,'  .' | 
|   |  .\ : :   : '/ /        .--'.  ' ; |   :     : .'___,/    ,'  ,---.'   | 
.   :  |: | |   '   ,        /__./ \ : | .   |  ;. / |    :     |   |   |   .' 
|   : :   / '   |  /     .--'.  '   \' . .   ; /--`  ;    |.';  ;   :   :  :   
|   |   \ : '   ;  ;    /___/ \ |    ' ' ;   | ;     `----'  |  |   :   |  |-, 
;   | |`-'  :   '   \   ;   \  \;      : |   : |         '   :  ;   |   :  ;/| 
|   | ;     |   |    '   \   ;  `      | .   | '___      |   |  '   |   |   .' 
:   ' |     '   : |.  \   .   \    .\  ; '   ; : .'|     '   :  |   '   :  '   
:   : :     |   | '_\.'    \   \   ' \ | '   | '/  :     ;   |.'    |   |  |   
|   | :     '   : |         :   '  |--"  |   :    /      '---'      |   :  \   
`---'.|     ;   |,'          \   \ ;      \   \ .'                  |   | ,'   
  `---`     '---'             '---"        `---`                    `----'     
                                                                               

呆呆鸟：这一次我将赢回所有！

(Generating the games, please wait a moment.)
                                                               
'''

# 全局调试开关 - 正式部署时设为False
DEBUG = False

class Suit:
    HEARTS = '♥'
    DIAMONDS = '♦' 
    CLUBS = '♣'
    SPADES = '♠'

class Rank:
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return str(self)

class HandStrength:
    # 短牌规则：同花大于葫芦
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FULL_HOUSE = 6
    FLUSH = 7  # 短牌中同花大于葫芦
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9

class ShortDeckPokerGame:
    def __init__(self):
        self.deck = self.create_short_deck()
        self.player_cards = []
        self.bot_cards = []
        self.community_cards = []
        self.used_cards = set()
    
    def create_short_deck(self):
        """创建短牌牌组（移除2-5）"""
        deck = []
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            for rank in [Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, 
                        Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]:
                deck.append(Card(rank, suit))
        random.shuffle(deck)
        return deck
    
    def deal_card(self):
        if not self.deck:
            self.deck = self.create_short_deck()
        card = self.deck.pop()
        while str(card) in self.used_cards:
            if not self.deck:
                self.deck = self.create_short_deck()
            card = self.deck.pop()
        self.used_cards.add(str(card))
        return card
    
    def setup_game(self):
        """设置游戏：发手牌和4张公共牌"""
        self.player_cards = [self.deal_card(), self.deal_card()]
        self.bot_cards = []
        for _ in range(3):
            self.bot_cards.append([self.deal_card(), self.deal_card()])
        
        self.community_cards = []
        for _ in range(4):
            self.community_cards.append(self.deal_card())
    
    def rank_to_value(self, rank):
        """将牌面转换为数值（短牌特化）"""
        rank_values = {
            Rank.SIX: 6, Rank.SEVEN: 7, Rank.EIGHT: 8, Rank.NINE: 9,
            Rank.TEN: 10, Rank.JACK: 11, Rank.QUEEN: 12, Rank.KING: 13,
            Rank.ACE: 14
        }
        return rank_values[rank]
    
    def get_hand_name(self, strength):
        """获取手牌名称"""
        names = {
            HandStrength.HIGH_CARD: "高牌",
            HandStrength.ONE_PAIR: "一对",
            HandStrength.TWO_PAIR: "两对",
            HandStrength.THREE_OF_A_KIND: "三条",
            HandStrength.STRAIGHT: "顺子",
            HandStrength.FULL_HOUSE: "葫芦",
            HandStrength.FLUSH: "同花",
            HandStrength.FOUR_OF_A_KIND: "四条",
            HandStrength.STRAIGHT_FLUSH: "同花顺"
        }
        return names.get(strength, "未知")
    
    def calculate_hand_strength(self, cards):
        """计算手牌强度（短牌特化）"""
        if len(cards) != 7:
            return (HandStrength.HIGH_CARD, 0)
        
        # 按花色和点数分组
        ranks = {}
        suits = {}
        
        for card in cards:
            rank_val = self.rank_to_value(card.rank)
            suit_val = card.suit
            
            if rank_val not in ranks:
                ranks[rank_val] = 0
            ranks[rank_val] += 1
            
            if suit_val not in suits:
                suits[suit_val] = 0
            suits[suit_val] += 1
        
        # 检查同花
        flush = False
        flush_suit = None
        for suit, count in suits.items():
            if count >= 5:
                flush = True
                flush_suit = suit
                break
        
        # 检查顺子（短牌特化，不考虑A作为5的情况）
        straight = False
        straight_high = 0
        sorted_ranks = sorted(ranks.keys())
        
        # 检查普通顺子
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                straight = True
                straight_high = sorted_ranks[i+4]
        
        # 检查同花顺
        if flush and straight:
            # 验证同花顺
            flush_cards = [card for card in cards if card.suit == flush_suit]
            flush_ranks = sorted([self.rank_to_value(card.rank) for card in flush_cards])
            
            for i in range(len(flush_ranks) - 4):
                if flush_ranks[i+4] - flush_ranks[i] == 4:
                    return (HandStrength.STRAIGHT_FLUSH, flush_ranks[i+4])
        
        # 检查四条
        for rank, count in ranks.items():
            if count == 4:
                return (HandStrength.FOUR_OF_A_KIND, rank)
        
        # 检查同花（短牌中同花大于葫芦）
        if flush:
            flush_ranks = sorted([self.rank_to_value(card.rank) for card in cards if card.suit == flush_suit], reverse=True)
            return (HandStrength.FLUSH, flush_ranks[0])
        
        # 检查葫芦
        three_of_kind = None
        pair = None
        for rank, count in sorted(ranks.items(), reverse=True):
            if count == 3 and three_of_kind is None:
                three_of_kind = rank
            elif count >= 2 and pair is None and rank != three_of_kind:
                pair = rank
        
        if three_of_kind is not None and pair is not None:
            return (HandStrength.FULL_HOUSE, three_of_kind)
        
        # 检查顺子
        if straight:
            return (HandStrength.STRAIGHT, straight_high)
        
        # 检查三条
        if three_of_kind is not None:
            return (HandStrength.THREE_OF_A_KIND, three_of_kind)
        
        # 检查两对
        pairs = []
        for rank, count in sorted(ranks.items(), reverse=True):
            if count == 2:
                pairs.append(rank)
            if len(pairs) == 2:
                return (HandStrength.TWO_PAIR, max(pairs))
        
        # 检查一对
        if len(pairs) == 1:
            return (HandStrength.ONE_PAIR, pairs[0])
        
        # 高牌
        return (HandStrength.HIGH_CARD, max(ranks.keys()))
    
    def compare_hands(self, hand1, hand2):
        """比较两手牌的强度"""
        strength1, value1 = hand1
        strength2, value2 = hand2
        
        if strength1 > strength2:
            return 1
        elif strength1 < strength2:
            return -1
        else:
            if value1 > value2:
                return 1
            elif value1 < value2:
                return -1
            else:
                return 0
    
    def calculate_outs(self):
        """计算outs数量 - CTF核心逻辑"""
        outs = 0
        outs_cards = []  # 存储所有正确的outs牌
        
        # 创建所有可能的牌（短牌）
        all_cards = []
        for suit in [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]:
            for rank in [Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, 
                        Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]:
                all_cards.append(Card(rank, suit))
        
        # 计算玩家当前手牌强度（没有最后一张牌）
        player_current_hand = self.player_cards + self.community_cards
        player_current_strength = self.calculate_hand_strength(player_current_hand + [Card(Rank.SIX, Suit.HEARTS)])  # 随便加一张牌
        if DEBUG:
            print(f"[DEBUG] 玩家当前手牌强度: {self.get_hand_name(player_current_strength[0])}")
        
        # 遍历所有可能的最后一张牌
        for card in all_cards:
            if str(card) in self.used_cards:
                continue
            
            # 构建完整的7张牌
            player_final_hand = self.player_cards + self.community_cards + [card]
            player_strength = self.calculate_hand_strength(player_final_hand)
            
            # 检查是否能击败所有bot
            can_win_all = True
            bot_names = ["Chestnut", "Lion", "Doraemon"]
            
            for i, bot_hand in enumerate(self.bot_cards):
                bot_final_hand = bot_hand + self.community_cards + [card]
                bot_strength = self.calculate_hand_strength(bot_final_hand)
                
                if self.compare_hands(player_strength, bot_strength) <= 0:
                    can_win_all = False
                    if DEBUG:
                        print(f"[DEBUG] 河牌 {card} 无法击败 {bot_names[i]} (玩家: {self.get_hand_name(player_strength[0])}, {bot_names[i]}: {self.get_hand_name(bot_strength[0])})")
                    # 注意：这里不break，因为我们想检查所有bot
            
            if can_win_all:
                outs += 1
                outs_cards.append(card)
                if DEBUG:
                    print(f"[DEBUG] 河牌 {card} 是outs (玩家最终手牌: {self.get_hand_name(player_strength[0])})")
        
        if DEBUG:
            print(f"[DEBUG] 总outs数量: {outs}")
        return outs, outs_cards

def generate_poker_games():
    """生成5个短牌德州扑克游戏"""
    games = []
    for _ in range(5):
        game = ShortDeckPokerGame()
        game.setup_game()
        games.append(game)
    return games

if __name__ == "__main__":
    print(BANNER)
    
    # 生成短牌德州扑克游戏
    games = generate_poker_games()
    correct_answers = []
    outs_cards_list = []
    
    for game in games:
        outs, outs_cards = game.calculate_outs()
        correct_answers.append(outs)
        outs_cards_list.append(outs_cards)
    
    # 打印所有正确答案（测试用）
    if DEBUG:
        print("\n[DEBUG] 所有游戏的正确答案:")
        for i, answer in enumerate(correct_answers, 1):
            print(f"[DEBUG] 游戏 {i}: {answer}")
        print()
    
    correct_count = 0
    
    for i, game in enumerate(games, 1):
        print(f"\n========= Game {i} =========")
        print(f"你的手牌: {game.player_cards[0]}, {game.player_cards[1]}")
        print(f"公共手牌: {', '.join(str(card) for card in game.community_cards)}")
        print("对手手牌:")
        bot_names = ["Chestnut", "Lion", "Doraemon"]
        for j, bot_hand in enumerate(game.bot_cards):
            print(f"  {bot_names[j]}: {bot_hand[0]}, {bot_hand[1]}")
        
        # 打印当前游戏的正确答案（测试用）
        if DEBUG:
            print(f"[DEBUG] 游戏 {i} 的正确答案是: {correct_answers[i-1]}")
        
        try:
            user_answer = int(input(f"\n请输入本局的outs: ").strip())
            
            if user_answer == correct_answers[i-1]:
                print("正确!")
                correct_count += 1
            else:
                print(f"\n错误，正确的outs: {correct_answers[i-1]}.")
                print(f"所有可以赢的牌如下: {', '.join(str(card) for card in outs_cards_list[i-1])}")
                print("Program exiting...")
                exit(1)
                
        except ValueError:
            print("Error: 请输入一个整数.")
            print("Program exiting...")
            exit(1)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            exit(1)
    
    # 如果所有答案都正确
    if correct_count == 5:
        print("\n恭喜你获得了梦境扑克大赛的胜利!")
        print(f"Here is your flag: {flag}")
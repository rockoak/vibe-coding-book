"""
十三支撲克牌遊戲 (Chinese Poker - Thirteen Cards)
完整版：單人對電腦，含圖形化介面、AI 對手、特殊規則
"""

import random
import tkinter as tk
from tkinter import messagebox
from enum import Enum
from typing import List, Tuple, Dict
from collections import Counter

# ==================== 常數定義 ====================

class Suit(Enum):
    """花色"""
    SPADE = "♠"    # 黑桃
    HEART = "♥"    # 紅心
    DIAMOND = "♦"  # 方塊
    CLUB = "♣"     # 梅花

class Rank(Enum):
    """點數"""
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    
    def __init__(self, value, display):
        self._value = value
        self._display = display
    
    @property
    def value(self):
        return self._value
    
    @property
    def display(self):
        return self._display

class HandType(Enum):
    """牌型"""
    HIGH_CARD = (0, "散牌")
    ONE_PAIR = (1, "一對")
    TWO_PAIR = (2, "兩對")
    THREE_OF_KIND = (3, "三條")
    STRAIGHT = (4, "順子")
    FLUSH = (5, "同花")
    FULL_HOUSE = (6, "葫蘆")
    FOUR_OF_KIND = (7, "鐵支")
    STRAIGHT_FLUSH = (8, "同花順")
    
    def __init__(self, value, display):
        self._value = value
        self._display = display
    
    @property
    def value(self):
        return self._value
    
    @property
    def display(self):
        return self._display

# ==================== 撲克牌類別 ====================

class Card:
    """撲克牌"""
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.suit.value}{self.rank.display}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def __lt__(self, other):
        return self.rank.value < other.rank.value
    
    def __hash__(self):
        return hash((self.suit, self.rank))

class Deck:
    """牌組"""
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """重置牌組"""
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.shuffle()
    
    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
    
    def deal(self, num: int) -> List[Card]:
        """發牌"""
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards

# ==================== 牌型判斷系統 ====================

class HandEvaluator:
    """牌型評估器"""
    
    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Tuple[HandType, List[int]]:
        """
        評估牌型
        返回：(牌型, 比較用的點數列表)
        """
        if len(cards) not in [3, 5]:
            raise ValueError("牌數必須是 3 或 5 張")
        
        # 排序牌
        sorted_cards = sorted(cards, key=lambda c: c.rank.value, reverse=True)
        ranks = [c.rank.value for c in sorted_cards]
        suits = [c.suit for c in sorted_cards]
        
        # 計算點數出現次數
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)
        
        # 判斷是否同花
        is_flush = len(set(suits)) == 1
        
        # 判斷是否順子
        is_straight = HandEvaluator._is_straight(ranks)
        
        # 5 張牌的牌型判斷
        if len(cards) == 5:
            if is_straight and is_flush:
                return (HandType.STRAIGHT_FLUSH, [max(ranks)])
            if counts == [4, 1]:
                four_rank = [r for r, c in rank_counts.items() if c == 4][0]
                kicker = [r for r, c in rank_counts.items() if c == 1][0]
                return (HandType.FOUR_OF_KIND, [four_rank, kicker])
            if counts == [3, 2]:
                three_rank = [r for r, c in rank_counts.items() if c == 3][0]
                pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
                return (HandType.FULL_HOUSE, [three_rank, pair_rank])
            if is_flush:
                return (HandType.FLUSH, sorted(ranks, reverse=True))
            if is_straight:
                return (HandType.STRAIGHT, [max(ranks)])
            if counts == [3, 1, 1]:
                three_rank = [r for r, c in rank_counts.items() if c == 3][0]
                kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
                return (HandType.THREE_OF_KIND, [three_rank] + kickers)
            if counts == [2, 2, 1]:
                pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
                kicker = [r for r, c in rank_counts.items() if c == 1][0]
                return (HandType.TWO_PAIR, pairs + [kicker])
            if counts == [2, 1, 1, 1]:
                pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
                kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
                return (HandType.ONE_PAIR, [pair_rank] + kickers)
            return (HandType.HIGH_CARD, sorted(ranks, reverse=True))
        
        # 3 張牌的牌型判斷（頭墩）
        else:
            if counts == [3]:
                return (HandType.THREE_OF_KIND, [ranks[0]])
            if counts == [2, 1]:
                pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
                kicker = [r for r, c in rank_counts.items() if c == 1][0]
                return (HandType.ONE_PAIR, [pair_rank, kicker])
            return (HandType.HIGH_CARD, sorted(ranks, reverse=True))
    
    @staticmethod
    def _is_straight(ranks: List[int]) -> bool:
        """判斷是否為順子"""
        if len(ranks) != 5:
            return False
        
        sorted_ranks = sorted(set(ranks))
        if len(sorted_ranks) != 5:
            return False
        
        # 一般順子
        if sorted_ranks[-1] - sorted_ranks[0] == 4:
            return True
        
        # A-2-3-4-5 的特殊順子
        if sorted_ranks == [2, 3, 4, 5, 14]:
            return True
        
        return False
    
    @staticmethod
    def compare_hands(hand1: Tuple[HandType, List[int]], 
                     hand2: Tuple[HandType, List[int]]) -> int:
        """
        比較兩手牌
        返回：1 (hand1贏), -1 (hand2贏), 0 (平手)
        """
        type1, values1 = hand1
        type2, values2 = hand2
        
        # 先比牌型
        if type1.value > type2.value:
            return 1
        elif type1.value < type2.value:
            return -1
        
        # 牌型相同，比點數
        for v1, v2 in zip(values1, values2):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        
        return 0

# ==================== AI 配牌系統 ====================

class AIPlayer:
    """AI 玩家（簡化版）"""
    
    @staticmethod
    def arrange_cards(cards: List[Card]) -> Tuple[List[Card], List[Card], List[Card]]:
        """
        AI 自動配牌
        返回：(頭墩3張, 中墩5張, 尾墩5張)
        簡化策略：從強到弱分配到尾墩、中墩、頭墩
        """
        if len(cards) != 13:
            raise ValueError("必須是 13 張牌")
        
        # 排序所有牌
        sorted_cards = sorted(cards, key=lambda c: c.rank.value, reverse=True)
        
        # 簡單策略：最強的 5 張給尾墩，中間 5 張給中墩，最弱 3 張給頭墩
        # 這是一個簡化版本，實際應該要更複雜的邏輯
        back = sorted_cards[:5]
        middle = sorted_cards[5:10]
        front = sorted_cards[10:13]
        
        return (front, middle, back)

# ==================== 計分系統 ====================

class ScoreCalculator:
    """計分系統"""
    
    # 特殊牌型加分
    SPECIAL_SCORES = {
        # 頭墩特殊牌型
        ('front', HandType.THREE_OF_KIND): 3,
        # 中墩特殊牌型
        ('middle', HandType.FULL_HOUSE): 2,
        ('middle', HandType.FOUR_OF_KIND): 8,
        ('middle', HandType.STRAIGHT_FLUSH): 10,
        # 尾墩特殊牌型
        ('back', HandType.FOUR_OF_KIND): 4,
        ('back', HandType.STRAIGHT_FLUSH): 5,
    }
    
    @staticmethod
    def calculate_score(player_hands: Dict, ai_hands: Dict) -> Tuple[int, str]:
        """
        計算分數
        返回：(玩家得分, 詳細說明)
        正數表示玩家贏，負數表示 AI 贏
        """
        details = []
        total_score = 0
        
        # 檢查是否相公（牌型不符合規則）
        player_valid = ScoreCalculator._is_valid_arrangement(
            player_hands['front'][0], 
            player_hands['middle'][0], 
            player_hands['back'][0]
        )
        ai_valid = ScoreCalculator._is_valid_arrangement(
            ai_hands['front'][0], 
            ai_hands['middle'][0], 
            ai_hands['back'][0]
        )
        
        if not player_valid:
            details.append("⚠️ 玩家相公！（牌型不合規則）")
            return (-6, "\n".join(details))
        
        if not ai_valid:
            details.append("⚠️ AI 相公！（牌型不合規則）")
            return (6, "\n".join(details))
        
        # 比較三墩
        front_result = HandEvaluator.compare_hands(player_hands['front'], ai_hands['front'])
        middle_result = HandEvaluator.compare_hands(player_hands['middle'], ai_hands['middle'])
        back_result = HandEvaluator.compare_hands(player_hands['back'], ai_hands['back'])
        
        wins = sum([1 for r in [front_result, middle_result, back_result] if r == 1])
        losses = sum([1 for r in [front_result, middle_result, back_result] if r == -1])
        
        # 基本分數
        base_score = wins - losses
        total_score += base_score
        
        details.append(f"基本分數: {base_score} 水（贏{wins}墩 - 輸{losses}墩）")
        
        # 全壘打（三墩全贏）
        if wins == 3:
            total_score += 3
            details.append("🎉 全壘打！額外 +3 水")
        elif losses == 3:
            total_score -= 3
            details.append("💻 AI 全壘打！額外 -3 水")
        
        # 打槍（某一墩特別強）
        # 特殊牌型加分
        player_bonus = ScoreCalculator._calculate_special_bonus(player_hands)
        ai_bonus = ScoreCalculator._calculate_special_bonus(ai_hands)
        
        if player_bonus > 0:
            details.append(f"✨ 玩家特殊牌型加分: +{player_bonus} 水")
        if ai_bonus > 0:
            details.append(f"✨ AI 特殊牌型加分: -{ai_bonus} 水")
        
        total_score += player_bonus - ai_bonus
        
        details.append(f"\n💰 總分: {total_score:+d} 水")
        
        return (total_score, "\n".join(details))
    
    @staticmethod
    def _is_valid_arrangement(front: Tuple, middle: Tuple, back: Tuple) -> bool:
        """檢查配牌是否合法（頭墩 ≤ 中墩 ≤ 尾墩）"""
        front_type, front_values = front
        middle_type, middle_values = middle
        back_type, back_values = back
        
        # 比較牌型大小
        if front_type.value > middle_type.value:
            return False
        if middle_type.value > back_type.value:
            return False
        
        # 相同牌型比點數
        if front_type == middle_type:
            if front_values[0] > middle_values[0]:
                return False
        if middle_type == back_type:
            if middle_values[0] > back_values[0]:
                return False
        
        return True
    
    @staticmethod
    def _calculate_special_bonus(hands: Dict) -> int:
        """計算特殊牌型加分"""
        bonus = 0
        
        for position in ['front', 'middle', 'back']:
            hand_type = hands[position][0]
            key = (position, hand_type)
            if key in ScoreCalculator.SPECIAL_SCORES:
                bonus += ScoreCalculator.SPECIAL_SCORES[key]
        
        return bonus

# ==================== 圖形化介面 ====================

class ThirteenPokerGUI:
    """十三支遊戲圖形介面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎴 十三支撲克牌遊戲")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2d5016")
        
        # 遊戲狀態
        self.deck = Deck()
        self.player_cards = []
        self.ai_cards = []
        self.selected_cards = []
        
        # 玩家配牌
        self.player_front = []
        self.player_middle = []
        self.player_back = []
        
        # 按鈕引用
        self.card_buttons = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """建立使用者介面"""
        # 標題
        title_label = tk.Label(
            self.root, 
            text="🎴 十三支撲克牌遊戲", 
            font=("微軟正黑體", 24, "bold"),
            bg="#2d5016",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # AI 區域
        ai_frame = tk.LabelFrame(
            self.root,
            text="💻 電腦",
            font=("微軟正黑體", 14),
            bg="#2d5016",
            fg="white"
        )
        ai_frame.pack(pady=10, padx=20, fill="x")
        
        self.ai_label = tk.Label(
            ai_frame,
            text="等待發牌...",
            font=("微軟正黑體", 12),
            bg="#2d5016",
            fg="white"
        )
        self.ai_label.pack(pady=10)
        
        # 玩家配牌區域
        player_arrange_frame = tk.LabelFrame(
            self.root,
            text="👤 你的配牌",
            font=("微軟正黑體", 14),
            bg="#2d5016",
            fg="white"
        )
        player_arrange_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # 頭墩
        front_frame = tk.Frame(player_arrange_frame, bg="#2d5016")
        front_frame.pack(pady=5)
        tk.Label(
            front_frame,
            text="頭墩（3張）:",
            font=("微軟正黑體", 12),
            bg="#2d5016",
            fg="yellow"
        ).pack(side="left", padx=5)
        self.front_cards_label = tk.Label(
            front_frame,
            text="",
            font=("Courier New", 14),
            bg="#2d5016",
            fg="white"
        )
        self.front_cards_label.pack(side="left")
        
        # 中墩
        middle_frame = tk.Frame(player_arrange_frame, bg="#2d5016")
        middle_frame.pack(pady=5)
        tk.Label(
            middle_frame,
            text="中墩（5張）:",
            font=("微軟正黑體", 12),
            bg="#2d5016",
            fg="yellow"
        ).pack(side="left", padx=5)
        self.middle_cards_label = tk.Label(
            middle_frame,
            text="",
            font=("Courier New", 14),
            bg="#2d5016",
            fg="white"
        )
        self.middle_cards_label.pack(side="left")
        
        # 尾墩
        back_frame = tk.Frame(player_arrange_frame, bg="#2d5016")
        back_frame.pack(pady=5)
        tk.Label(
            back_frame,
            text="尾墩（5張）:",
            font=("微軟正黑體", 12),
            bg="#2d5016",
            fg="yellow"
        ).pack(side="left", padx=5)
        self.back_cards_label = tk.Label(
            back_frame,
            text="",
            font=("Courier New", 14),
            bg="#2d5016",
            fg="white"
        )
        self.back_cards_label.pack(side="left")
        
        # 玩家手牌區域
        hand_frame = tk.LabelFrame(
            self.root,
            text="你的手牌（點擊選擇）",
            font=("微軟正黑體", 14),
            bg="#2d5016",
            fg="white"
        )
        hand_frame.pack(pady=10, padx=20, fill="x")
        
        self.cards_frame = tk.Frame(hand_frame, bg="#2d5016")
        self.cards_frame.pack(pady=10)
        
        # 控制按鈕區域
        control_frame = tk.Frame(self.root, bg="#2d5016")
        control_frame.pack(pady=10)
        
        tk.Button(
            control_frame,
            text="🎲 開始遊戲",
            font=("微軟正黑體", 14, "bold"),
            command=self.start_game,
            bg="#4CAF50",
            fg="white",
            width=12,
            height=2
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="➡️ 放入頭墩",
            font=("微軟正黑體", 12),
            command=lambda: self.place_cards("front"),
            bg="#2196F3",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="➡️ 放入中墩",
            font=("微軟正黑體", 12),
            command=lambda: self.place_cards("middle"),
            bg="#FF9800",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="➡️ 放入尾墩",
            font=("微軟正黑體", 12),
            command=lambda: self.place_cards("back"),
            bg="#F44336",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="🤖 AI 自動配牌",
            font=("微軟正黑體", 12),
            command=self.auto_arrange,
            bg="#9C27B0",
            fg="white",
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="✅ 確認比牌",
            font=("微軟正黑體", 14, "bold"),
            command=self.show_result,
            bg="#FF5722",
            fg="white",
            width=12,
            height=2
        ).pack(side="left", padx=5)
    
    def start_game(self):
        """開始遊戲"""
        # 重置狀態
        self.deck.reset()
        self.player_cards = self.deck.deal(13)
        self.ai_cards = self.deck.deal(13)
        self.selected_cards = []
        self.player_front = []
        self.player_middle = []
        self.player_back = []
        
        # 顯示玩家手牌
        self.display_player_cards()
        self.update_arrangement_display()
        
        self.ai_label.config(text="電腦已拿到 13 張牌，正在思考配牌...")
        
        messagebox.showinfo("遊戲開始", "已發牌！請開始配牌\n\n規則：頭墩3張 ≤ 中墩5張 ≤ 尾墩5張")
    
    def display_player_cards(self):
        """顯示玩家手牌"""
        # 清空舊按鈕
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.card_buttons = []
        
        # 排序手牌
        sorted_cards = sorted(self.player_cards, key=lambda c: (c.suit.value, c.rank.value))
        
        # 創建牌按鈕
        for i, card in enumerate(sorted_cards):
            color = "red" if card.suit in [Suit.HEART, Suit.DIAMOND] else "black"
            btn = tk.Button(
                self.cards_frame,
                text=str(card),
                font=("Courier New", 16, "bold"),
                fg=color,
                bg="white",
                width=5,
                height=2,
                command=lambda c=card: self.toggle_card(c)
            )
            btn.grid(row=i // 7, column=i % 7, padx=3, pady=3)
            self.card_buttons.append((btn, card))
    
    def toggle_card(self, card: Card):
        """切換卡片選擇狀態"""
        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)
        
        # 更新按鈕外觀
        for btn, c in self.card_buttons:
            if c == card:
                if card in self.selected_cards:
                    btn.config(relief="sunken", bg="lightblue")
                else:
                    btn.config(relief="raised", bg="white")
    
    def place_cards(self, position: str):
        """將選擇的牌放入指定墩位"""
        if not self.selected_cards:
            messagebox.showwarning("提示", "請先選擇要放入的牌！")
            return
        
        max_cards = 3 if position == "front" else 5
        current_list = getattr(self, f"player_{position}")
        
        if len(current_list) + len(self.selected_cards) > max_cards:
            messagebox.showwarning(
                "提示", 
                f"{'頭墩' if position == 'front' else '中墩' if position == 'middle' else '尾墩'}最多{max_cards}張牌！"
            )
            return
        
        # 移動牌
        for card in self.selected_cards:
            current_list.append(card)
            self.player_cards.remove(card)
        
        self.selected_cards = []
        self.display_player_cards()
        self.update_arrangement_display()
    
    def auto_arrange(self):
        """AI 自動配牌"""
        if not self.player_cards or len(self.player_cards) != 13:
            messagebox.showwarning("提示", "請先開始遊戲！")
            return
        
        # 重置配牌
        all_cards = self.player_cards + self.player_front + self.player_middle + self.player_back
        self.player_front, self.player_middle, self.player_back = AIPlayer.arrange_cards(all_cards)
        self.player_cards = []
        self.selected_cards = []
        
        self.display_player_cards()
        self.update_arrangement_display()
        
        messagebox.showinfo("完成", "AI 已為你自動配牌！")
    
    def update_arrangement_display(self):
        """更新配牌顯示"""
        self.front_cards_label.config(text=" ".join([str(c) for c in self.player_front]))
        self.middle_cards_label.config(text=" ".join([str(c) for c in self.player_middle]))
        self.back_cards_label.config(text=" ".join([str(c) for c in self.player_back]))
    
    def show_result(self):
        """顯示比牌結果"""
        # 檢查是否配牌完成
        if len(self.player_front) != 3 or len(self.player_middle) != 5 or len(self.player_back) != 5:
            messagebox.showwarning("提示", "請先完成配牌！\n頭墩3張、中墩5張、尾墩5張")
            return
        
        # AI 配牌
        ai_front, ai_middle, ai_back = AIPlayer.arrange_cards(self.ai_cards)
        
        # 評估牌型
        player_hands = {
            'front': HandEvaluator.evaluate_hand(self.player_front),
            'middle': HandEvaluator.evaluate_hand(self.player_middle),
            'back': HandEvaluator.evaluate_hand(self.player_back)
        }
        
        ai_hands = {
            'front': HandEvaluator.evaluate_hand(ai_front),
            'middle': HandEvaluator.evaluate_hand(ai_middle),
            'back': HandEvaluator.evaluate_hand(ai_back)
        }
        
        # 計算分數
        score, details = ScoreCalculator.calculate_score(player_hands, ai_hands)
        
        # 顯示結果
        result_text = "="*50 + "\n"
        result_text += "🎴 比牌結果\n"
        result_text += "="*50 + "\n\n"
        
        result_text += "👤 你的牌型：\n"
        result_text += f"  頭墩: {' '.join([str(c) for c in self.player_front])} - {player_hands['front'][0].display}\n"
        result_text += f"  中墩: {' '.join([str(c) for c in self.player_middle])} - {player_hands['middle'][0].display}\n"
        result_text += f"  尾墩: {' '.join([str(c) for c in self.player_back])} - {player_hands['back'][0].display}\n\n"
        
        result_text += "💻 電腦的牌型：\n"
        result_text += f"  頭墩: {' '.join([str(c) for c in ai_front])} - {ai_hands['front'][0].display}\n"
        result_text += f"  中墩: {' '.join([str(c) for c in ai_middle])} - {ai_hands['middle'][0].display}\n"
        result_text += f"  尾墩: {' '.join([str(c) for c in ai_back])} - {ai_hands['back'][0].display}\n\n"
        
        result_text += "="*50 + "\n"
        result_text += details + "\n"
        result_text += "="*50 + "\n"
        
        if score > 0:
            result_text += f"\n🎉 你贏了 {score} 水！"
        elif score < 0:
            result_text += f"\n😢 你輸了 {abs(score)} 水！"
        else:
            result_text += "\n🤝 平手！"
        
        # 創建結果視窗
        result_window = tk.Toplevel(self.root)
        result_window.title("比牌結果")
        result_window.geometry("600x500")
        result_window.configure(bg="#2d5016")
        
        text_widget = tk.Text(
            result_window,
            font=("Courier New", 11),
            bg="white",
            fg="black",
            wrap="word"
        )
        text_widget.pack(padx=20, pady=20, fill="both", expand=True)
        text_widget.insert("1.0", result_text)
        text_widget.config(state="disabled")
        
        tk.Button(
            result_window,
            text="關閉",
            font=("微軟正黑體", 12),
            command=result_window.destroy,
            bg="#4CAF50",
            fg="white",
            width=10
        ).pack(pady=10)

# ==================== 主程式 ====================

def main():
    """主程式入口"""
    root = tk.Tk()
    app = ThirteenPokerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

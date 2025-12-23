"""
core/fibonacci_logic.py
Mathematical utilities for the Phi-Chain consensus, including Fibonacci sequence and Golden Ratio calculations.
"""
import math
from decimal import Decimal, getcontext

# Set precision for Decimal operations
getcontext().prec = 50

class PhiMath:
    """
    A class for mathematical operations related to the Golden Ratio (Phi) and 
    the Fibonacci sequence, used in the Phi-Chain consensus.
    """

    def __init__(self):
        # Pre-calculate the Golden Ratio for efficiency
        self._phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)

    def golden_ratio(self, precision: int = 10) -> Decimal:
        """Returns the Golden Ratio (Phi) with specified precision."""
        return self._phi.quantize(Decimal('1e-' + str(precision)))

    def fibonacci(self, n: int) -> int:
        """
        Calculates the nth Fibonacci number using an iterative approach.
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def fibonacci_sequence(self, start: int, count: int) -> List[int]:
        """
        Generates a sequence of Fibonacci numbers starting from the 'start' index.
        """
        sequence = []
        for i in range(start, start + count):
            sequence.append(self.fibonacci(i))
        return sequence

    def fibonacci_distribution(self, total_reward: int, count: int) -> List[int]:
        """
        Distributes a total reward among 'count' participants based on 
        Fibonacci sequence proportions.
        """
        if count <= 0:
            return []
        
        # Get the first 'count' Fibonacci numbers (starting from F1=1)
        fib_numbers = self.fibonacci_sequence(1, count)
        
        # Calculate the total sum of the Fibonacci numbers
        total_fib = sum(fib_numbers)
        
        if total_fib == 0:
            return [0] * count
        
        # Distribute the reward proportionally
        rewards = []
        remaining_reward = total_reward
        
        for i in range(count):
            # Calculate the proportional share using Decimal for precision
            share = Decimal(fib_numbers[i]) / Decimal(total_fib)
            reward_amount = int(share * Decimal(total_reward))
            rewards.append(reward_amount)
            remaining_reward -= reward_amount
            
        # Distribute any remaining reward (due to integer truncation) to the first participant
        if rewards:
            rewards[0] += remaining_reward
            
        return rewards

# To avoid circular dependency in the PhiConsensus class, we will not import 
# the PhiMath class here, but rather ensure it is imported correctly in 
# phi_validator.py and blockchain.py.
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
import time
import json

# Placeholder for the Block and Blockchain classes which will be in blockchain.py
# This is necessary for the PhiMath class to be complete.
# The actual Block and Blockchain classes will be created in the next step.

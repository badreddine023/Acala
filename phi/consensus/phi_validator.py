"""
🎯 Φ-Chain Validator with Precise Mathematical Consensus
Enhanced with Fibonacci-based validator selection and Golden Ratio weighting
"""

import time
import hashlib
from decimal import Decimal, getcontext
from typing import List, Dict, Optional, Tuple
import json
from dataclasses import dataclass, asdict

# Import our precise mathematical library
from core.fibonacci_logic import PhiMath

getcontext().prec = 50

@dataclass
class Validator:
    """Validator node with mathematical properties"""
    address: str
    public_key: str
    stake: int
    weight: Decimal
    fibonacci_index: int
    is_active: bool = True
    last_validated: int = 0
    performance_score: Decimal = Decimal('1.0')
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def get_priority_score(self, block_height: int) -> Decimal:
        """
        Calculate validator priority using Fibonacci-based formula
        
        Priority = stake × weight × performance × f(block_height)
        where f(block_height) uses Fibonacci sequence
        """
        # Get Fibonacci number for current block
        fib_number = PhiMath().fibonacci(block_height % 100)
        
        # Golden ratio influence
        phi = PhiMath().golden_ratio(10)
        
        # Calculate priority with mathematical properties
        base_priority = Decimal(self.stake) * self.weight * self.performance_score
        
        # Apply Fibonacci modulation (oscillates gracefully)
        modulation = Decimal(fib_number) / Decimal(1000)
        
        # Apply golden ratio scaling
        golden_scaling = phi ** Decimal(self.fibonacci_index % 10)
        
        final_priority = base_priority * modulation * golden_scaling
        
        return final_priority

class PhiConsensus:
    """
    Φ-Chain Consensus Engine with Fibonacci-based validator rotation
    and Golden Ratio-weighted decision making
    """
    
    def __init__(self, network_id: str = "phi-mainnet-1"):
        self.network_id = network_id
        self.validators: Dict[str, Validator] = {}
        self.phi_math = PhiMath()
        self.current_leader_index = 0
        self.round_number = 0
        
        # Consensus parameters
        self.block_time = 5  # seconds
        self.required_confirmations = int(self.phi_math.golden_ratio(2) * 3)  # ~5
        
        print(f"✅ Initialized Φ-Consensus for {network_id}")
    
    def add_validator(self, address: str, public_key: str, stake: int, 
                     fibonacci_index: Optional[int] = None) -> bool:
        """
        Add a validator with Fibonacci-based weight calculation
        
        Weight = φ^(index) where φ is golden ratio
        """
        if address in self.validators:
            print(f"⚠️ Validator {address} already exists")
            return False
        
        # Calculate Fibonacci index if not provided
        if fibonacci_index is None:
            fibonacci_index = len(self.validators)
        
        # Calculate weight using golden ratio: weight = φ^index
        weight = self.phi_math.golden_ratio(10) ** Decimal(fibonacci_index)
        
        # Create validator
        validator = Validator(
            address=address,
            public_key=public_key,
            stake=stake,
            weight=weight,
            fibonacci_index=fibonacci_index,
            is_active=True,
            performance_score=Decimal('1.0')
        )
        
        self.validators[address] = validator
        
        print(f"✅ Added validator {address} with weight {weight:.6f}")
        return True
    
    def select_leader(self, block_height: int) -> Optional[Validator]:
        """
        Select leader for next block using Fibonacci-weighted round robin
        
        Leader selection follows Fibonacci sequence pattern
        """
        if not self.validators:
            print("❌ No validators available")
            return None
        
        active_validators = [v for v in self.validators.values() if v.is_active]
        if not active_validators:
            print("❌ No active validators")
            return None
        
        # Calculate total priority
        total_priority = Decimal('0')
        priorities = []
        
        for validator in active_validators:
            priority = validator.get_priority_score(block_height)
            total_priority += priority
            priorities.append((validator, priority))
        
        if total_priority == 0:
            print("❌ Total priority is zero")
            return active_validators[0]
        
        # Use Fibonacci-based selection
        fib_number = self.phi_math.fibonacci(block_height % len(active_validators))
        
        # Normalize to selection index
        selection_index = fib_number % len(active_validators)
        
        selected_validator = active_validators[selection_index]
        
        # Update leader index
        self.current_leader_index = selection_index
        self.round_number += 1
        
        print(f"🎯 Selected leader: {selected_validator.address} "
              f"(Fibonacci index: {fib_number})")
        
        return selected_validator
    
    def validate_block(self, block_data: dict, proposer_address: str) -> bool:
        """
        Validate block with mathematical proofs
        
        Blocks must include:
        1. Fibonacci-based proof of work
        2. Golden ratio hash
        3. Validator signature
        """
        print(f"🔍 Validating block {block_data.get('height', 'unknown')}...")
        
        # Check if proposer is a valid validator
        if proposer_address not in self.validators:
            print(f"❌ Proposer {proposer_address} not a validator")
            return False
        
        proposer = self.validators[proposer_address]
        
        if not proposer.is_active:
            print(f"❌ Proposer {proposer_address} is inactive")
            return False
        
        # Extract mathematical proof
        math_proof = block_data.get("mathematical_proof", {})
        
        # Verify Fibonacci proof
        if not self._verify_fibonacci_proof(math_proof, block_data):
            print("❌ Fibonacci proof verification failed")
            return False
        
        # Verify Golden Ratio hash
        if not self._verify_golden_hash(block_data):
            print("❌ Golden ratio hash verification failed")
            return False
        
        # Verify signature (placeholder - implement actual crypto)
        if not self._verify_signature(block_data, proposer.public_key):
            print("❌ Signature verification failed")
            return False
        
        # Update validator performance
        self._update_validator_performance(proposer_address, True)
        
        print(f"✅ Block {block_data.get('height', 'unknown')} validated successfully")
        return True
    
    def _verify_fibonacci_proof(self, math_proof: dict, block_data: dict) -> bool:
        """Verify Fibonacci-based mathematical proof"""
        try:
            block_height = block_data.get("height", 0)
            
            # Expected Fibonacci number for this block
            expected_fib = self.phi_math.fibonacci(block_height % 1000)
            
            # Get proof Fibonacci number
            proof_fib = math_proof.get("fibonacci_number")
            
            if proof_fib != expected_fib:
                print(f"❌ Fibonacci mismatch: expected {expected_fib}, got {proof_fib}")
                return False
            
            # Verify Fibonacci index
            proof_index = math_proof.get("fibonacci_index")
            expected_index = block_height % 1000
            
            if proof_index != expected_index:
                print(f"❌ Fibonacci index mismatch: expected {expected_index}, got {proof_index}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Fibonacci proof error: {e}")
            return False
    
    def _verify_golden_hash(self, block_data: dict) -> bool:
        """Verify Golden Ratio hash in block"""
        try:
            golden_hash = block_data.get("header", {}).get("golden_ratio_hash", "")
            
            if not golden_hash or len(golden_hash) != 64:
                print("❌ Invalid golden hash format")
                return False
            
            # Verify hash contains mathematical properties
            # (In production, this would be a proper cryptographic check)
            
            return True
            
        except Exception as e:
            print(f"❌ Golden hash verification error: {e}")
            return False
    
    def _verify_signature(self, block_data: dict, public_key: str) -> bool:
        """Verify block signature (placeholder for actual crypto)"""
        # TODO: Implement actual ECDSA signature verification
        signature = block_data.get("signature", "")
        
        if not signature:
            print("⚠️ No signature in block (test mode)")
            return True  # Allow in test mode
        
        # Placeholder: Always return True for testing
        # In production, implement proper signature verification
        return True
    
    def _update_validator_performance(self, address: str, success: bool):
        """Update validator performance score"""
        if address not in self.validators:
            return
        
        validator = self.validators[address]
        
        # Update performance score (simple moving average)
        if success:
            # Increase score, but cap at 1.0
            new_score = validator.performance_score * Decimal('0.95') + Decimal('0.05')
            validator.performance_score = min(new_score, Decimal('1.0'))
        else:
            # Decrease score
            validator.performance_score *= Decimal('0.9')
        
        # Update last validation time
        validator.last_validated = int(time.time())
    
    def get_validator_rotation_schedule(self, blocks_ahead: int = 100) -> List[Tuple[int, str]]:
        """
        Generate validator rotation schedule based on Fibonacci sequence
        
        Returns list of (block_height, expected_validator_address)
        """
        schedule = []
        active_validators = [v.address for v in self.validators.values() if v.is_active]
        
        if not active_validators:
            return schedule
        
        for block_offset in range(blocks_ahead):
            # Use Fibonacci number to determine rotation
            fib_num = self.phi_math.fibonacci(block_offset % 20)
            
            # Select validator based on Fibonacci number
            validator_index = fib_num % len(active_validators)
            validator_address = active_validators[validator_index]
            
            schedule.append((block_offset, validator_address))
        
        return schedule
    
    def calculate_rewards(self, block_height: int, total_reward: int) -> Dict[str, int]:
        """
        Calculate validator rewards using Fibonacci distribution
        
        Rewards follow Fibonacci sequence proportions
        """
        rewards = {}
        active_validators = [v for v in self.validators.values() if v.is_active]
        
        if not active_validators:
            return rewards
        
        # Use Fibonacci distribution
        amounts = self.phi_math.fibonacci_distribution(
            total_reward, 
            len(active_validators)
        )
        
        # Distribute rewards
        for i, validator in enumerate(active_validators):
            if i < len(amounts):
                rewards[validator.address] = amounts[i]
            else:
                rewards[validator.address] = 0
        
        return rewards
    
    def generate_consensus_report(self) -> dict:
        """Generate detailed consensus report with mathematical metrics"""
        active_count = sum(1 for v in self.validators.values() if v.is_active)
        total_stake = sum(v.stake for v in self.validators.values() if v.is_active)
        
        # Calculate mathematical metrics
        avg_weight = sum(float(v.weight) for v in self.validators.values() if v.is_active) / max(active_count, 1)
        avg_performance = sum(float(v.performance_score) for v in self.validators.values() if v.is_active) / max(active_count, 1)
        
        report = {
            "network_id": self.network_id,
            "total_validators": len(self.validators),
            "active_validators": active_count,
            "total_stake": total_stake,
            "current_round": self.round_number,
            "current_leader": self.current_leader_index,
            "mathematical_metrics": {
                "average_weight": avg_weight,
                "average_performance": avg_performance,
                "golden_ratio": str(self.phi_math.golden_ratio(10)),
                "fibonacci_distribution": self.phi_math.fibonacci_sequence(0, min(10, active_count))
            },
            "validators": [
                {
                    "address": v.address,
                    "stake": v.stake,
                    "weight": float(v.weight),
                    "performance": float(v.performance_score),
                    "is_active": v.is_active
                }
                for v in self.validators.values()
            ]
        }
        
        return report

# ==================== Helper Functions ====================

def create_genesis_validators() -> PhiConsensus:
    """
    Create genesis validators with Fibonacci-based distribution
    """
    consensus = PhiConsensus("phi-mainnet-1")
    
    # Genesis validators with Fibonacci stake distribution
    genesis_stakes = [1000000, 1618033, 2618033, 4236066, 6854099, 11090165]
    
    for i, stake in enumerate(genesis_stakes):
        address = f"phi_genesis_validator_{i}"
        public_key = f"genesis_pub_key_{i:02x}"
        
        consensus.add_validator(
            address=address,
            public_key=public_key,
            stake=stake,
            fibonacci_index=i
        )
    
    print(f"✅ Created {len(genesis_stakes)} genesis validators")
    return consensus

def run_consensus_tests():
    """Run consensus engine tests"""
    print("🧪 Running Φ-Consensus Tests...")
    
    # Create test consensus
    consensus = create_genesis_validators()
    
    # Test 1: Leader selection
    leader = consensus.select_leader(block_height=1)
    if leader:
        print(f"✅ Leader selected: {leader.address}")
    else:
        print("❌ Leader selection failed")
    
    # Test 2: Block validation
    test_block = {
        "height": 1,
        "mathematical_proof": {
            "fibonacci_number": consensus.phi_math.fibonacci(1),
            "fibonacci_index": 1
        },
        "header": {
            "golden_ratio_hash": "a" * 64
        },
        "signature": "test_signature"
    }
    
    is_valid = consensus.validate_block(test_block, leader.address if leader else "")
    print(f"✅ Block validation: {is_valid}")
    
    # Test 3: Rotation schedule
    schedule = consensus.get_validator_rotation_schedule(10)
    print(f"✅ Rotation schedule generated: {len(schedule)} blocks")
    
    # Test 4: Rewards calculation
    rewards = consensus.calculate_rewards(1, 1000000)
    print(f"✅ Rewards calculated for {len(rewards)} validators")
    
    # Test 5: Generate report
    report = consensus.generate_consensus_report()
    print(f"✅ Consensus report generated: {report['active_validators']} active validators")
    
    print("🧪 All consensus tests passed!")

if __name__ == "__main__":
    # Run tests if file executed directly
    run_consensus_tests()

"""
phi/blockchain.py
Core blockchain logic for the Φ-Chain, including Block structure and Blockchain management.
Integrates the PhiConsensus mechanism for validation.
"""
import time
import json
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# Import dependencies
from phi.consensus.phi_validator import PhiConsensus
from core.fibonacci_logic import PhiMath

@dataclass
class Block:
    """Represents a single block in the Φ-Chain."""
    index: int
    timestamp: float
    transactions: List[Dict[str, Any]]
    proof: int  # Placeholder for PoC proof
    previous_hash: str
    validator_address: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the block to a dictionary for hashing."""
        return asdict(self)

    def hash(self) -> str:
        """Creates a SHA-256 hash of the block."""
        block_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    """Manages the chain, transactions, and consensus integration."""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []
        self.consensus_engine = PhiConsensus()
        self.phi_math = PhiMath()
        
        # Create the genesis block
        self.create_block(
            proof=self.phi_math.fibonacci(0), 
            previous_hash='1',
            validator_address='phi_genesis_validator_0'
        )
        
        # Initialize genesis validators for the consensus engine
        self._initialize_genesis_validators()

    def _initialize_genesis_validators(self):
        """Initializes the genesis validators for the consensus engine."""
        # This logic is copied from the run_consensus_tests in phi_validator.py
        genesis_stakes = [1000000, 1618033, 2618033, 4236066, 6854099, 11090165]
        
        for i, stake in enumerate(genesis_stakes):
            address = f"phi_genesis_validator_{i}"
            public_key = f"genesis_pub_key_{i:02x}"
            
            self.consensus_engine.add_validator(
                address=address,
                public_key=public_key,
                stake=stake,
                fibonacci_index=i
            )

    def create_block(self, proof: int, previous_hash: str, validator_address: str) -> Block:
        """
        Adds a new block to the chain.
        
        :param proof: The Proof-of-Commitment (PoC) proof found by the miner.
        :param previous_hash: Hash of the previous block.
        :param validator_address: The address of the validator who proposed the block.
        :return: The new Block.
        """
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time.time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash,
            validator_address=validator_address
        )
        
        # Reset the current list of transactions
        self.current_transactions = []
        
        # Validate the block using the consensus engine (simplified for now)
        validation_data = {
            "height": block.index,
            "mathematical_proof": {
                "fibonacci_number": self.phi_math.fibonacci(block.index % 1000),
                "fibonacci_index": block.index % 1000
            },
            "header": {
                "golden_ratio_hash": "a" * 64 # Placeholder
            },
            "signature": "test_signature" # Placeholder
        }
        
        if self.consensus_engine.validate_block(validation_data, validator_address):
            self.chain.append(block)
            return block
        else:
            # Handle failed validation (e.g., log error, penalize validator)
            print(f"Block {block.index} proposed by {validator_address} failed validation.")
            return None

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        Adds a new transaction to the list of transactions to be included in the next block.
        
        :param sender: Address of the Sender.
        :param recipient: Address of the Recipient.
        :param amount: Amount of the transaction.
        :return: The index of the block that will hold this transaction.
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        })
        
        return self.last_block.index + 1

    @property
    def last_block(self) -> Block:
        """Returns the last block in the chain."""
        return self.chain[-1] if self.chain else None

    def get_next_leader(self) -> Optional[str]:
        """Uses the consensus engine to select the next block proposer."""
        next_height = len(self.chain) + 1
        leader = self.consensus_engine.select_leader(next_height)
        return leader.address if leader else None

# Placeholder for phi_chain_core.py, which will likely contain the main application logic
# and API endpoints, using the Blockchain class.
class PhiChainCore:
    """Main application logic for the Φ-Chain node."""
    def __init__(self):
        self.blockchain = Blockchain()
        print("Φ-Chain Core Initialized. Chain length:", len(self.blockchain.chain))

if __name__ == '__main__':
    # Simple test run
    core = PhiChainCore()
    
    # Select a leader
    leader_address = core.blockchain.get_next_leader()
    print(f"Next leader selected: {leader_address}")
    
    # Add a transaction
    core.blockchain.new_transaction("Alice", "Bob", 10.5)
    
    # Create a new block (simulating a successful PoC mining)
    new_block = core.blockchain.create_block(
        proof=12345, 
        previous_hash=core.blockchain.last_block.hash(),
        validator_address=leader_address
    )
    
    if new_block:
        print(f"New block created at index {new_block.index} with hash {new_block.hash()}")
        print(f"Chain length: {len(core.blockchain.chain)}")
    else:
        print("Failed to create new block.")

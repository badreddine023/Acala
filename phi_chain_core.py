"""
phi_chain_core.py
Main application entry point for the Φ-Chain node.
This file will eventually host the API and main node runner logic.
"""
from phi.blockchain import PhiChainCore

if __name__ == '__main__':
    # Initialize the core node logic
    node = PhiChainCore()
    
    # Placeholder for starting the API server and node runner
    print("Φ-Chain Node is running...")
    
    # Example usage:
    # print(f"Current block count: {len(node.blockchain.chain)}")
    # print(f"Next block proposer: {node.blockchain.get_next_leader()}")
    
    # In a real application, this would start a continuous loop 
    # for mining/validation and an API server.

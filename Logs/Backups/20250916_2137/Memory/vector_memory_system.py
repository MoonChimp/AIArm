"""
Enhanced Memory System with Vector Embeddings
Provides persistent memory and context management for the multi-agent system
"""

import os
import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import pickle
from pathlib import Path

class VectorMemorySystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory_dir = config.get('memory_dir', 'D:/AIArm/Memory')
        self.db_path = os.path.join(self.memory_dir, 'agent_memory.db')
        self.vector_cache = {}
        self.embedding_dimension = 384  # Standard for small local models
        
        # Create memory directory
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                agent_id TEXT,
                content TEXT,
                memory_type TEXT,
                importance REAL,
                embedding BLOB,
                metadata TEXT,
                created_at TIMESTAMP,
                last_accessed TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                agent_id TEXT,
                message TEXT,
                response TEXT,
                context TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_states (
                agent_id TEXT PRIMARY KEY,
                current_context TEXT,
                active_memories TEXT,
                performance_metrics TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_graphs (
                id TEXT PRIMARY KEY,
                subject TEXT,
                predicate TEXT,
                object TEXT,
                confidence REAL,
                source_memory_id TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_memory(self, agent_id: str, content: str, memory_type: str, 
                    importance: float = 0.5, metadata: Dict[str, Any] = None) -> str:
        """Store a new memory with vector embedding"""
        try:
            # Generate unique ID
            memory_id = hashlib.sha256(f"{agent_id}_{content}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
            
            # Generate embedding (placeholder - replace with local embedding model)
            embedding = self._generate_embedding(content)
            
            # Prepare metadata
            metadata_json = json.dumps(metadata or {})
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories 
                (id, agent_id, content, memory_type, importance, embedding, metadata, created_at, last_accessed, access_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_id, agent_id, content, memory_type, importance,
                pickle.dumps(embedding), metadata_json, 
                datetime.now(), datetime.now(), 0
            ))
            
            conn.commit()
            conn.close()
            
            return memory_id
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            return None
    
    def retrieve_memories(self, agent_id: str, query: str, limit: int = 10, 
                         memory_type: str = None) -> List[Dict[str, Any]]:
        """Retrieve relevant memories using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            # Get all memories for agent
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if memory_type:
                cursor.execute('''
                    SELECT id, content, memory_type, importance, embedding, metadata, created_at, access_count
                    FROM memories 
                    WHERE agent_id = ? AND memory_type = ?
                    ORDER BY importance DESC, created_at DESC
                ''', (agent_id, memory_type))
            else:
                cursor.execute('''
                    SELECT id, content, memory_type, importance, embedding, metadata, created_at, access_count
                    FROM memories 
                    WHERE agent_id = ?
                    ORDER BY importance DESC, created_at DESC
                ''', (agent_id,))
            
            memories = cursor.fetchall()
            conn.close()
            
            # Calculate similarities and rank
            memory_scores = []
            for memory in memories:
                memory_id, content, mem_type, importance, embedding_blob, metadata, created_at, access_count = memory
                
                # Deserialize embedding
                stored_embedding = pickle.loads(embedding_blob)
                
                # Calculate similarity
                similarity = self._cosine_similarity(query_embedding, stored_embedding)
                
                # Combine similarity with importance and recency
                recency_factor = self._calculate_recency_factor(created_at)
                final_score = (similarity * 0.6) + (importance * 0.3) + (recency_factor * 0.1)
                
                memory_scores.append({
                    'id': memory_id,
                    'content': content,
                    'type': mem_type,
                    'importance': importance,
                    'similarity': similarity,
                    'score': final_score,
                    'metadata': json.loads(metadata),
                    'created_at': created_at,
                    'access_count': access_count
                })
            
            # Sort by score and return top results
            memory_scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Update access counts
            self._update_memory_access([m['id'] for m in memory_scores[:limit]])
            
            return memory_scores[:limit]
            
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def store_conversation(self, session_id: str, agent_id: str, message: str, 
                          response: str, context: Dict[str, Any] = None) -> str:
        """Store conversation for future reference"""
        try:
            conversation_id = hashlib.sha256(f"{session_id}_{agent_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations 
                (id, session_id, agent_id, message, response, context, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                conversation_id, session_id, agent_id, message, response,
                json.dumps(context or {}), datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
            # Also store as memory for the agent
            self.store_memory(
                agent_id, 
                f"User: {message}\nAgent: {response}", 
                'conversation',
                importance=0.7,
                metadata={'session_id': session_id, 'conversation_id': conversation_id}
            )
            
            return conversation_id
            
        except Exception as e:
            print(f"Error storing conversation: {e}")
            return None
    
    def update_agent_context(self, agent_id: str, context: Dict[str, Any], 
                           active_memories: List[str] = None) -> bool:
        """Update agent's current context and active memories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO agent_states 
                (agent_id, current_context, active_memories, last_updated)
                VALUES (?, ?, ?, ?)
            ''', (
                agent_id,
                json.dumps(context),
                json.dumps(active_memories or []),
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error updating agent context: {e}")
            return False
    
    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Get agent's current context and active memories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT current_context, active_memories, last_updated
                FROM agent_states 
                WHERE agent_id = ?
            ''', (agent_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                context, active_memories, last_updated = result
                return {
                    'context': json.loads(context),
                    'active_memories': json.loads(active_memories),
                    'last_updated': last_updated
                }
            else:
                return {
                    'context': {},
                    'active_memories': [],
                    'last_updated': None
                }
                
        except Exception as e:
            print(f"Error getting agent context: {e}")
            return {'context': {}, 'active_memories': [], 'last_updated': None}
    
    def create_knowledge_graph_entry(self, subject: str, predicate: str, object_: str, 
                                   confidence: float, source_memory_id: str) -> str:
        """Create knowledge graph entry from memory"""
        try:
            kg_id = hashlib.sha256(f"{subject}_{predicate}_{object_}".encode()).hexdigest()[:16]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO knowledge_graphs 
                (id, subject, predicate, object, confidence, source_memory_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (kg_id, subject, predicate, object_, confidence, source_memory_id, datetime.now()))
            
            conn.commit()
            conn.close()
            
            return kg_id
            
        except Exception as e:
            print(f"Error creating knowledge graph entry: {e}")
            return None
    
    def query_knowledge_graph(self, subject: str = None, predicate: str = None, 
                            object_: str = None, min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """Query knowledge graph"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build dynamic query
            conditions = []
            params = []
            
            if subject:
                conditions.append("subject LIKE ?")
                params.append(f"%{subject}%")
            if predicate:
                conditions.append("predicate LIKE ?")
                params.append(f"%{predicate}%")
            if object_:
                conditions.append("object LIKE ?")
                params.append(f"%{object_}%")
            
            conditions.append("confidence >= ?")
            params.append(min_confidence)
            
            where_clause = " AND ".join(conditions)
            query = f'''
                SELECT subject, predicate, object, confidence, source_memory_id, created_at
                FROM knowledge_graphs 
                WHERE {where_clause}
                ORDER BY confidence DESC
            '''
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'subject': r[0],
                    'predicate': r[1],
                    'object': r[2],
                    'confidence': r[3],
                    'source_memory_id': r[4],
                    'created_at': r[5]
                }
                for r in results
            ]
            
        except Exception as e:
            print(f"Error querying knowledge graph: {e}")
            return []
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate vector embedding for text (placeholder implementation)"""
        # Simple hash-based embedding for now
        # In production, use local embedding model like sentence-transformers
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        
        # Convert hash to fixed-size vector
        embedding = np.array([
            int(hash_val[i:i+2], 16) / 255.0 
            for i in range(0, min(len(hash_val), self.embedding_dimension * 2), 2)
        ])
        
        # Pad or truncate to desired dimension
        if len(embedding) < self.embedding_dimension:
            embedding = np.pad(embedding, (0, self.embedding_dimension - len(embedding)))
        else:
            embedding = embedding[:self.embedding_dimension]
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        except:
            return 0.0
    
    def _calculate_recency_factor(self, created_at: str) -> float:
        """Calculate recency factor (0-1) based on creation time"""
        try:
            created_time = datetime.fromisoformat(created_at)
            now = datetime.now()
            days_old = (now - created_time).days
            
            # Exponential decay: newer memories get higher scores
            return max(0.1, np.exp(-days_old / 30))  # Half-life of ~30 days
        except:
            return 0.5
    
    def _update_memory_access(self, memory_ids: List[str]):
        """Update access count and timestamp for memories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for memory_id in memory_ids:
                cursor.execute('''
                    UPDATE memories 
                    SET access_count = access_count + 1, last_accessed = ?
                    WHERE id = ?
                ''', (datetime.now(), memory_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating memory access: {e}")
    
    def cleanup_old_memories(self, days_old: int = 90, min_importance: float = 0.3):
        """Clean up old, low-importance memories"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM memories 
                WHERE created_at < ? AND importance < ? AND access_count < 5
            ''', (cutoff_date, min_importance))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up memories: {e}")
            return 0
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count memories by agent
            cursor.execute('''
                SELECT agent_id, COUNT(*), AVG(importance), MAX(access_count)
                FROM memories 
                GROUP BY agent_id
            ''')
            agent_stats = {row[0]: {'count': row[1], 'avg_importance': row[2], 'max_access': row[3]} 
                          for row in cursor.fetchall()}
            
            # Total counts
            cursor.execute('SELECT COUNT(*) FROM memories')
            total_memories = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM conversations')
            total_conversations = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM knowledge_graphs')
            total_kg_entries = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_memories': total_memories,
                'total_conversations': total_conversations,
                'total_knowledge_graph_entries': total_kg_entries,
                'agent_statistics': agent_stats,
                'database_path': self.db_path,
                'embedding_dimension': self.embedding_dimension
            }
            
        except Exception as e:
            print(f"Error getting memory statistics: {e}")
            return {}

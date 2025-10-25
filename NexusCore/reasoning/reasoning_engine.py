#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reasoning Engine - Core of Nexus-LIRA Intelligence

This is what makes LIRA truly THINK, not just respond.
Implements hierarchical reasoning with:
- Task decomposition
- Evidence gathering
- Logical inference
- Hypothesis testing
- Meta-cognition
"""

import json
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

class ReasoningNode:
    """
    A single node in the reasoning tree
    Represents one step in the reasoning process
    """
    def __init__(self, question: str, level: int = 0, parent=None):
        self.question = question
        self.level = level  # Depth in reasoning hierarchy
        self.parent = parent
        self.children: List['ReasoningNode'] = []
        self.evidence: List[str] = []
        self.hypotheses: List[Dict] = []
        self.conclusion: Optional[str] = None
        self.confidence: float = 0.0
        self.reasoning_steps: List[str] = []

    def add_child(self, child: 'ReasoningNode'):
        """Add a sub-question to explore"""
        self.children.append(child)
        child.parent = self

    def add_evidence(self, evidence: str):
        """Add evidence gathered for this node"""
        self.evidence.append(evidence)

    def add_hypothesis(self, hypothesis: str, confidence: float):
        """Add a hypothesis with confidence level"""
        self.hypotheses.append({
            "hypothesis": hypothesis,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self) -> Dict:
        """Convert reasoning node to dictionary"""
        return {
            "question": self.question,
            "level": self.level,
            "evidence": self.evidence,
            "hypotheses": self.hypotheses,
            "conclusion": self.conclusion,
            "confidence": self.confidence,
            "reasoning_steps": self.reasoning_steps,
            "children": [child.to_dict() for child in self.children]
        }


class ReasoningEngine:
    """
    Hierarchical Reasoning Engine for Nexus-LIRA

    This is THE BRAIN - makes Nexus truly intelligent
    """

    def __init__(self,
                 ollama_base: str = "http://localhost:11434",
                 model: str = "nexusai-a0-coder1.0:latest"):

        self.ollama_base = ollama_base
        self.model = model

        # Reasoning configuration
        self.max_depth = 5  # Maximum reasoning hierarchy depth
        self.confidence_threshold = 0.7  # Minimum confidence to accept conclusion
        self.max_hypotheses = 3  # Max hypotheses to consider per node

        # Reasoning modes
        self.modes = {
            "deductive": self._reason_deductive,
            "inductive": self._reason_inductive,
            "abductive": self._reason_abductive,
            "analogical": self._reason_analogical
        }

        print("[ReasoningEngine] Initialized - LIRA Brain Online")
        print(f"[ReasoningEngine] Max Reasoning Depth: {self.max_depth}")
        print(f"[ReasoningEngine] Reasoning Modes: {', '.join(self.modes.keys())}")

    def reason(self, question: str, context: Optional[Dict] = None) -> Dict:
        """
        Main reasoning entry point

        Takes a question and returns a complete reasoning chain with conclusion

        Args:
            question: The question or problem to reason about
            context: Additional context/knowledge

        Returns:
            Complete reasoning tree with conclusion
        """
        print(f"\n[ReasoningEngine] 🧠 REASONING MODE ACTIVATED")
        print(f"[ReasoningEngine] Question: {question}")

        # Step 1: Determine reasoning mode
        mode = self._select_reasoning_mode(question, context)
        print(f"[ReasoningEngine] Reasoning Mode: {mode}")

        # Step 2: Create root reasoning node
        root = ReasoningNode(question, level=0)

        # Step 3: Decompose into sub-questions (hierarchical reasoning)
        self._decompose_question(root, context)

        # Step 4: Gather evidence for each node
        self._gather_evidence_recursive(root, context)

        # Step 5: Generate hypotheses
        self._generate_hypotheses_recursive(root, context)

        # Step 6: Evaluate and synthesize conclusion
        self._synthesize_conclusion_recursive(root, context)

        # Step 7: Meta-cognitive evaluation
        self._meta_evaluate(root)

        print(f"[ReasoningEngine] ✓ Reasoning complete")
        print(f"[ReasoningEngine] Conclusion: {root.conclusion[:100]}...")
        print(f"[ReasoningEngine] Confidence: {root.confidence:.2%}")

        return {
            "question": question,
            "reasoning_tree": root.to_dict(),
            "conclusion": root.conclusion,
            "confidence": root.confidence,
            "reasoning_mode": mode,
            "depth": self._get_tree_depth(root),
            "num_steps": self._count_reasoning_steps(root)
        }

    def _select_reasoning_mode(self, question: str, context: Optional[Dict]) -> str:
        """
        Determine which reasoning mode to use

        - Deductive: General → Specific (logical rules)
        - Inductive: Specific → General (pattern recognition)
        - Abductive: Effect → Cause (best explanation)
        - Analogical: Similar → Transfer (pattern matching)
        """
        prompt = f"""Analyze this question and determine the best reasoning approach.

Question: {question}

Reasoning modes:
- deductive: Use logical rules to reach certain conclusions
- inductive: Find patterns from examples to general principles
- abductive: Find the best explanation for observations
- analogical: Apply knowledge from similar situations

Which mode is best? Respond with just the mode name."""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a reasoning strategist. Choose the best approach."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=20
            )

            if response.status_code == 200:
                mode = response.json().get("message", {}).get("content", "").strip().lower()
                if mode in self.modes:
                    return mode

        except Exception as e:
            print(f"[ReasoningEngine] Mode selection error: {e}")

        return "deductive"  # Default

    def _decompose_question(self, node: ReasoningNode, context: Optional[Dict]):
        """
        Break down complex question into sub-questions
        This creates the hierarchical structure
        """
        if node.level >= self.max_depth:
            return  # Max depth reached

        prompt = f"""Break this question into 2-4 simpler sub-questions.

Main question: {node.question}

Generate sub-questions that, when answered, will help answer the main question.
Respond in JSON format:
{{
  "sub_questions": ["question1", "question2", "question3"]
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a question decomposer. Break complex questions into simpler ones."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.4, "num_ctx": 4096}
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                # Extract JSON
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    sub_questions = data.get("sub_questions", [])

                    # Create child nodes
                    for sub_q in sub_questions[:4]:  # Limit to 4
                        child = ReasoningNode(sub_q, level=node.level + 1, parent=node)
                        node.add_child(child)

                        # Recursively decompose children
                        if node.level < self.max_depth - 1:
                            self._decompose_question(child, context)

        except Exception as e:
            print(f"[ReasoningEngine] Decomposition error: {e}")

    def _gather_evidence_recursive(self, node: ReasoningNode, context: Optional[Dict]):
        """
        Gather evidence for this node and all children
        Evidence = facts, data, observations relevant to the question
        """
        # Gather evidence for current node
        prompt = f"""Gather relevant evidence/facts to help answer this question.

Question: {node.question}

Context: {json.dumps(context) if context else 'None'}

List 3-5 key pieces of evidence or relevant facts.
Be specific and factual."""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an evidence gatherer. Provide factual, relevant information."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.5}
                },
                timeout=30
            )

            if response.status_code == 200:
                evidence = response.json().get("message", {}).get("content", "")
                node.add_evidence(evidence)

        except Exception as e:
            print(f"[ReasoningEngine] Evidence gathering error: {e}")

        # Recursively gather evidence for children
        for child in node.children:
            self._gather_evidence_recursive(child, context)

    def _generate_hypotheses_recursive(self, node: ReasoningNode, context: Optional[Dict]):
        """
        Generate possible hypotheses/answers for each node
        """
        prompt = f"""Based on this question and evidence, generate {self.max_hypotheses} possible hypotheses or answers.

Question: {node.question}
Evidence: {node.evidence}

For each hypothesis, assess confidence (0-1).
Respond in JSON:
{{
  "hypotheses": [
    {{"text": "hypothesis 1", "confidence": 0.8}},
    {{"text": "hypothesis 2", "confidence": 0.6}}
  ]
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a hypothesis generator. Propose plausible explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.7}
                },
                timeout=30
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    hypotheses = data.get("hypotheses", [])

                    for hyp in hypotheses:
                        node.add_hypothesis(hyp.get("text", ""), hyp.get("confidence", 0.5))

        except Exception as e:
            print(f"[ReasoningEngine] Hypothesis generation error: {e}")

        # Recursively generate for children
        for child in node.children:
            self._generate_hypotheses_recursive(child, context)

    def _synthesize_conclusion_recursive(self, node: ReasoningNode, context: Optional[Dict]):
        """
        Synthesize conclusions from bottom-up
        Children conclusions feed into parent reasoning
        """
        # First, synthesize all children
        for child in node.children:
            self._synthesize_conclusion_recursive(child, context)

        # Gather child conclusions
        child_conclusions = [
            f"Sub-question: {child.question}\nConclusion: {child.conclusion}"
            for child in node.children
            if child.conclusion
        ]

        prompt = f"""Synthesize a final conclusion for this question.

Question: {node.question}
Evidence: {json.dumps(node.evidence)}
Hypotheses: {json.dumps(node.hypotheses)}
Sub-conclusions: {json.dumps(child_conclusions) if child_conclusions else 'None'}

Provide:
1. A clear, concise conclusion
2. Confidence level (0-1)
3. Reasoning steps you used

Respond in JSON:
{{
  "conclusion": "your conclusion",
  "confidence": 0.85,
  "reasoning_steps": ["step1", "step2"]
}}"""

        try:
            response = requests.post(
                f"{self.ollama_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a conclusion synthesizer. Combine evidence into clear answers."},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.4, "num_ctx": 8192}
                },
                timeout=45
            )

            if response.status_code == 200:
                content = response.json().get("message", {}).get("content", "")

                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    node.conclusion = data.get("conclusion", "")
                    node.confidence = float(data.get("confidence", 0.5))
                    node.reasoning_steps = data.get("reasoning_steps", [])

        except Exception as e:
            print(f"[ReasoningEngine] Synthesis error: {e}")
            node.conclusion = "Unable to reach conclusion"
            node.confidence = 0.0

    def _meta_evaluate(self, root: ReasoningNode):
        """
        Meta-cognitive evaluation:
        - Is the reasoning sound?
        - Are we confident enough?
        - Did we miss anything?
        """
        print(f"\n[ReasoningEngine] 🔍 META-EVALUATION")

        # Check confidence
        if root.confidence < self.confidence_threshold:
            print(f"[ReasoningEngine] ⚠ Low confidence ({root.confidence:.2%})")
            print(f"[ReasoningEngine] Consider gathering more evidence")

        # Check reasoning depth
        depth = self._get_tree_depth(root)
        if depth < 2:
            print(f"[ReasoningEngine] ⚠ Shallow reasoning (depth={depth})")
            print(f"[ReasoningEngine] Consider deeper analysis")

        # Check completeness
        if not root.evidence:
            print(f"[ReasoningEngine] ⚠ No evidence gathered")

        if not root.hypotheses:
            print(f"[ReasoningEngine] ⚠ No hypotheses generated")

        print(f"[ReasoningEngine] ✓ Meta-evaluation complete")

    def _get_tree_depth(self, node: ReasoningNode) -> int:
        """Calculate maximum depth of reasoning tree"""
        if not node.children:
            return node.level
        return max(self._get_tree_depth(child) for child in node.children)

    def _count_reasoning_steps(self, node: ReasoningNode) -> int:
        """Count total reasoning steps in tree"""
        count = len(node.reasoning_steps)
        for child in node.children:
            count += self._count_reasoning_steps(child)
        return count

    # Specific reasoning modes
    def _reason_deductive(self, node: ReasoningNode, context: Optional[Dict]):
        """Deductive reasoning: General rules → Specific conclusion"""
        pass  # Implemented in main flow

    def _reason_inductive(self, node: ReasoningNode, context: Optional[Dict]):
        """Inductive reasoning: Specific examples → General principle"""
        pass  # Future enhancement

    def _reason_abductive(self, node: ReasoningNode, context: Optional[Dict]):
        """Abductive reasoning: Observation → Best explanation"""
        pass  # Future enhancement

    def _reason_analogical(self, node: ReasoningNode, context: Optional[Dict]):
        """Analogical reasoning: Similar situation → Transfer knowledge"""
        pass  # Future enhancement


if __name__ == "__main__":
    # Test the reasoning engine
    engine = ReasoningEngine()

    # Test question
    result = engine.reason(
        "Why should I use hierarchical reasoning in AI systems?",
        context={"domain": "AI architecture"}
    )

    print("\n" + "="*80)
    print("REASONING RESULT:")
    print("="*80)
    print(json.dumps(result, indent=2))

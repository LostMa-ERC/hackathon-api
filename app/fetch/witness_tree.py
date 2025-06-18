from typing import Generator

from app.core.db import GraphDB
from app.models.nodes import Document, Part, Place, Repository, Witness


class WitnessTreeBuilder:

    @classmethod
    def build_witness_query(cls, witness_id: int = None) -> str:
        basic = """
        MATCH (w:Witness){}
        OPTIONAL MATCH (w)-[]->(s:Scripta)
        RETURN w, s
        ORDER BY w.id
        """
        if witness_id:
            return basic.format(f" WHERE w.id = {witness_id}")
        else:
            return basic.format("")

    def __init__(self, db: GraphDB):
        self.db = db

    def get_witness(self, witness_id: int = None) -> Witness:
        query = self.build_witness_query(witness_id=witness_id)
        for witness_node, scripta_node in self.db.get_rows(query):
            return self.model_witness_data(
                witness_node=witness_node,
                scripta_node=scripta_node,
            )

    def iter_witnesses(self) -> Generator[Witness, None, None]:
        query = self.build_witness_query()
        for witness_node, scripta_node in self.db.get_rows(query):
            yield self.model_witness_data(
                witness_node=witness_node,
                scripta_node=scripta_node,
            )

    def get_witness_docs(self, witness_id: int) -> list[Document]:
        query = f"""
            MATCH (w:Witness) WHERE w.id = {witness_id}
            MATCH (w)-[:IsMaterializedOn]->(p:Part)
            -[:IsMaterializedOn]->(d:Document)
            OPTIONAL MATCH (d)-[:IsLocated]->(r:Repository)
            OPTIONAL MATCH (r)-[:IsLocated]->(pl:Place)
            RETURN
                d AS doc,
                r as repo,
                pl as place,
                collect(distinct(p)) AS parts
        """
        manuscripts = []
        # For each pair of documents and its parts,
        for doc, repo, place, part_list in self.db.get_rows(query):
            # Validate and model the repository's settlement
            if place:
                repo.update({"settlement": Place.model_validate(place)})

            # Validate and model the manuscript's repository
            if repo:
                repository = {"repository": Repository.model_validate(repo)}
                doc.update(repository)

            # Validate and model the manuscript's parts
            ordered_parts = sorted(
                [Part.model_validate(p) for p in part_list],
                key=lambda x: x.div_order,
                reverse=False,
            )
            witness_parts = {"witness_parts": ordered_parts}
            doc.update(witness_parts)
            manuscript = Document.model_validate(doc)
            manuscripts.append(manuscript)

        # Return all of the witness's manuscripts
        return manuscripts

    def model_witness_data(self, witness_node: dict, scripta_node: dict) -> Witness:
        witness_node.update({"scripta": scripta_node})
        witness_id = witness_node["id"]
        manuscripts = self.get_witness_docs(witness_id=witness_id)
        witness_node.update({"manuscripts": manuscripts})
        return Witness.model_validate(witness_node)

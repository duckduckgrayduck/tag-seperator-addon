"""
This Add-On takes a look at a document's tags and if any of them are comma delimited, splits them
"""
import time
from documentcloud.addon import AddOn


class SeperateTags(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        self.client.session.headers.update({"User-Agent": "Tag Seperator"})

        for document in self.get_documents():
            tags = document.data.get("_tag", [])
            if not tags:
                continue

            new_tags = []
            changed = False
            for tag in tags:
                if "," in tag:
                    changed = True
                    new_tags.extend(
                        part.strip() for part in tag.split(",") if part.strip()
                    )
                else:
                    new_tags.append(tag)

            if not changed:
                continue

            # In case a tag appears twice, only keep the first
            # Example: Tag1 Tag1,Tag2 should become Tag1 Tag2
            # Not Tag1 Tag1 Tag2
            document.data["_tag"] = list(set(new_tags))
            self.client.patch(
                f"documents/{document.id}/",
                json={"data": document.data},
            )


if __name__ == "__main__":
    SeperateTags().main()
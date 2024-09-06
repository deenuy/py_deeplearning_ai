import os
import shutil
from mkdocs.plugins import BasePlugin

class CopyExtraFiles(BasePlugin):
    def on_post_build(self, config):
        docs_dir = config['docs_dir']
        site_dir = config['site_dir']

        # Copy PDF files from lecture_notes
        src_dir = os.path.join(docs_dir, 'lecture_notes')
        dst_dir = os.path.join(site_dir, 'lecture_notes')
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        for file in os.listdir(src_dir):
            if file.endswith('.pdf'):
                shutil.copy2(os.path.join(src_dir, file), dst_dir)

        return
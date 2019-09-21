## ログ出力
from logging import getLogger, StreamHandler, Formatter, FileHandler

logger = getLogger(__name__)
logger.setLevel(20)

# ストリーム送信
sh = StreamHandler()
formatter = Formatter('%(asctime)s:[%(levelname)s] %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

# ログ出力をファイルに送信
fh = FileHandler('logging.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

import yaml
import pymysql
import logging
import pymysql.cursors

formatter = logging.Formatter("%(name)-12s %(levelname)-8s %(message)s")
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
LOG.addHandler(ch)


def get_history(franchise_id, user_id, limit):
    """Grabs records from the conversation history"""
    # Get a database configuration from a YAML file
    config = get_config("main/config/config.yaml")

    substitutions = {
        "user_id": user_id,
        "franchise_id": franchise_id,
        "limit": limit
    }
    return get_info(config, "history", **substitutions)


def get_config(config_file):
    """Get the database configuration"""
    with open(config_file, "r") as db_config:
        config = yaml.load(db_config)
    return config["mysql"]


def get_info(config, sql_file, **kwargs):
    """Get some basic information from the database"""
    conn = pymysql.connect(
        host=config["host"], port=3306, user=config["user"],
        passwd=config["passwd"], db=config["db"],
        cursorclass=pymysql.cursors.DictCursor)

    with open("main/src/db/templates/{}.sql".format(sql_file), "r") as template:
        sql = template.read()

    escape_sequence = "__"
    for k, v in kwargs.items():
        sql = sql.replace("{}{}".format(escape_sequence, k), str(v))

    LOG.debug("SQL:\n{}".format(sql))
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    return results

if __name__ == "__main__":
    config = get_config("main/config/config.yaml")
    substitutions = {
        "user_id": "989139",
        "franchise_id": "354285",
        "limit": "20"
    }

    results = get_info(config, "history", **substitutions)
    LOG.info("Results: {}".format(results))
    for result in results:
        print("{}".format(result["created"]))

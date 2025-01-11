"""The main entry point."""
import os
import time
from tqdm import tqdm
import sys
import sshtunnel
import pymysql
from dotenv import load_dotenv
import argparse
from reports.execute_query import ExecuteQuery
from  utils.hiv_queries import hiv_active, hiv_mortality, mmd_6months, mmd_3_5months, active_24months_before, active_12months_before, vl_suppression_num, vl_suppression_den
from utils.ncd_queries import ncd_active, ncd_died, ncd_active_12months_before, ncd_active_24months_before, ncd_visits, retention_in_care_for_ncd_at_12months, retention_in_care_for_ncd_at_24months 
from utils.mh_queries import mh_active, mh_visits, mh_mortality, mh_active_12months_before, mh_active_24months_before, retention_in_care_for_mh_at_12months, retention_in_care_for_mh_at_24months
load_dotenv()

def connect():
    try:
        with sshtunnel.SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(sql_ip, sql_port),
        ) as tunnel:
            try:
                conn = pymysql.connect(
                host=sql_ip,
                user=sql_username,
                passwd=sql_password,
                db=sql_main_database,
                port=tunnel.local_bind_port,
                )
                
                cursor_obj = conn.cursor()
                report_type = input("Is this an HIV report or  NCD report(Answers are: HIV/NCD/MH):")
                if report_type == "HIV":
                    orgindicatorsHIV = ExecuteQuery(cursor_obj, path)
                    funcs = [
                        orgindicatorsHIV.execute_query(hiv_active,site,'J'),
                        orgindicatorsHIV.execute_query(hiv_mortality,site,'I'),
                        orgindicatorsHIV.execute_query(mmd_6months,site,'H'),
                        orgindicatorsHIV.execute_query(mmd_3_5months,site,'G'),
                        orgindicatorsHIV.execute_query(active_24months_before,site,'F'),
                        orgindicatorsHIV.execute_query(active_12months_before,site,'D'),
                        orgindicatorsHIV.execute_count_query(vl_suppression_num,site, 'K'),
                        orgindicatorsHIV.execute_count_query(vl_suppression_den,site, 'L')
                        ]
                elif report_type == "NCD":
                    orgindicatorsNCD = ExecuteQuery(cursor_obj, path)
                    funcs = [
                        orgindicatorsNCD.execute_count_query(ncd_active,site,'H'),
                        orgindicatorsNCD.execute_count_query(ncd_died,site,'G'),
                        orgindicatorsNCD.execute_count_query(ncd_active_12months_before,site,'D'),
                        orgindicatorsNCD.execute_count_query(ncd_active_24months_before,site,'F'),
                        orgindicatorsNCD.execute_count_query(ncd_visits,site,'I'),
                        orgindicatorsNCD.execute_count_query(retention_in_care_for_ncd_at_12months,site,'C'),
                        orgindicatorsNCD.execute_count_query(retention_in_care_for_ncd_at_24months,site,'E')                                                
                    ]
                elif report_type == "MH":
                    orgindicatorsMH = ExecuteQuery(cursor_obj, path)
                    funcs = [
                        orgindicatorsMH.execute_count_query(mh_active,site,'H'),
                        orgindicatorsMH.execute_count_query(mh_visits,site,'I'),
                        orgindicatorsMH.execute_count_query(mh_mortality,site,'G'),
                        orgindicatorsMH.execute_count_query(mh_active_12months_before,site,'D'),
                        orgindicatorsMH.execute_count_query(mh_active_24months_before,site,'F'),
                        orgindicatorsMH.execute_count_query(retention_in_care_for_mh_at_12months,site,'C'),
                        orgindicatorsMH.execute_count_query(retention_in_care_for_mh_at_24months,site,'E')                                                
                    ]
                else:
                    sys.exit()
                for i in tqdm(range(len(funcs))):
                    funcs[i]
                cursor_obj.close()
                conn.close()
            except Exception as e:
                print(e)
    except sshtunnel.BaseSSHTunnelForwarderError:
        print("Make Sure you have internet connection")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type =str, help = 'path of the report')
    parser.add_argument('-s', type = str, help = "site of the report")
    args = parser.parse_args()

    if args.p is None:
        print("Please add file path")
    else:
        path = args.p

    if args.s == "Lower":
        site = 'Lower'
        sql_hostname = os.environ["SQL_HOSTNAME"]
        sql_username = os.environ["LOWER_SQL_USERNAME"]
        sql_password = os.environ["SQL_PASSWORD"]
        sql_main_database = os.environ["SQL_MAIN_DATABASE"]
        sql_port = os.environ["SQL_PORT"]
        sql_port = int(sql_port)
        ssh_host = os.environ["LOWER_SSH_HOST"]
        ssh_user = os.environ["LOWER_SSH_USER"]
        ssh_password = os.environ ["LOWER_SSH_PASSWORD"]
        ssh_port = os.environ["SSH_PORT"]
        ssh_port = int(ssh_port)
        sql_ip = os.environ["SQL_IP"]
        connect()
    elif args.s == "Upper":
        site = 'Upper'
         
        sql_hostname = os.environ["SQL_HOSTNAME"]
        sql_username = os.environ["SQL_USERNAME"]
        sql_password = os.environ["SQL_PASSWORD"]
        sql_main_database = os.environ["SQL_MAIN_DATABASE"]
        sql_port = os.environ["SQL_PORT"]
        sql_port = int(sql_port)
        ssh_host = os.environ["SSH_HOST"]
        ssh_user = os.environ["SSH_USER"]
        ssh_password = os.environ ["SSH_PASSWORD"]
        ssh_port = os.environ["SSH_PORT"]
        ssh_port = int(ssh_port)
        sql_ip = os.environ["SQL_IP"]
        connect()
    else:
        print('Please sepcifiy the site')

# connect()
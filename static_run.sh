#!/bin/bash

PATH_FL="./settings/filelist.txt"
PATH_CC="./settings/congestion_control.txt"
PATH_BUF="./settings/buffer_size.txt"
PATH_SCH="./settings/scheduler.txt"
PATH_DIR="./settings/directory.txt"

id=
# carr_type=0
expr_type=0
count_mobile=0
count_unicom=0
count_telcom=0

list_iface=()
# list_carrier=()
list_fl=()
list_cc=()
list_buf=()
list_sch=()

SERVERIP= 
root_dir="."

function get_iface_and_carrier ###### ????
{
	list_iface=()
	for iface in `ifconfig | grep eth | cut -c 1-4`; do
	if [ ${iface} = "eth1" ];
	then
		list_iface+=(${iface})
		SERVERIP=192.168.10.129
	elif [ ${iface} = "eth2" ];
	then
		list_iface+=(${iface})
		SERVERIP=192.168.20.129
	fi
	done
	
	echo "UP interfaces: ${list_iface[@]}"
	
	IFS=$'\n' list_fl=($(< ${PATH_FL}))
    IFS=$'\n' list_cc=($(< ${PATH_CC}))
    IFS=$'\n' list_buf=($(< ${PATH_BUF}))
    IFS=$'\n' list_sch=($(< ${PATH_SCH}))
	
	
}

# @param $1 - seconds to count down
# @param $2 - tip information
function countdown
{
    seconds=${1}
    while [[ ${seconds} -ge 0 ]]; do
	echo -ne "The ${2} will start in ${seconds} seconds...\033[0K\r"
	(( seconds -= 1 ))
	sleep 1
    done
}

function get_carrier_type
{
    string="There are %s interfaces connect to *%s*\nPlease check your interfaces and restart the program\n"
    
    if [[ "${count_mobile}" -gt 1 ]]; then
	printf "$string" ${count_mobile} "CHINA MOBILE"; exit
    elif [[ "${count_unicom}" -gt 1 ]]; then
	printf "$string" ${count_unicom} "CHINA UNICOM"; exit
    elif [[ "${count_telcom}" -gt 1 ]]; then
	printf "$string" ${count_telcom} "CHINA TELCOM"; exit
    else
	(( carr_type = count_mobile * 4 + count_unicom * 2 + count_telcom ))
	if [[ "${carr_type}" = 0 ]]; then
	    echo "There's no WiFi connection. Please check your connection and try again."
	    exit;
	fi
	echo carrier type = ${carr_type}
    fi
}

# @param $1 - file size 
# @param $2 - congestion control
# @param $3 - buffer size
# @param $4 - scheduler
function get_expr_type
{
    expr_type=0
    
    case ${1} in
	20K.dat    )   (( expr_type += 1 )) ;;
	200K.dat   )   (( expr_type += 2 )) ;;
	2M.dat     )   (( expr_type += 3 )) ;;
	20M.dat    )   (( expr_type += 4 )) ;;
	600M.dat   )   (( expr_type += 5 )) ;;
    esac
    
    case ${2} in
	lia        )   (( expr_type += 0 )) ;;
	olia       )   (( expr_type += 5 )) ;;
	reno       )   (( expr_type += 10 ));;
    esac

    case ${3} in
	16777216   )   (( expr_type += 0 )) ;;
    esac

    case ${4} in
	default    )   (( expr_type += 0 )) ;;
	roundrobin )   (( expr_type += 15 ));;
    esac
}

# @param $1 - the root directory path
# @param $2 - the train ID, for example C2008, G234, and so on
function load_env
{
    train_path=${1}/${2}
    if [[ -e "$2" ]]; then
	id=`ls -l ${train_path} | grep "^d" | wc -l`
	(( id++ ))
	echo "current id is ${id}"
    else
	id=1
	mkdir -p ${train_path}
	echo `date +%s.%N` > ${train_path}/train_start_time
	echo `date +%s.%N` > ${train_path}/train_end_time
    fi

    # sudo ifconfig wlan0 down

    
    # get_carrier_type
    # echo ${carr_type} > ${1}/${2}/carrier_type

    
    
    file=${list_fl[ $RANDOM % ${#list_fl[@]} ]}
    cc=${list_cc[ $RANDOM % ${#list_cc[@]} ]}
    buf=${list_buf[ $RANDOM % ${#list_buf[@]} ]}
    sch=${list_sch[ $RANDOM % ${#list_sch[@]} ]}

    echo ${list_fl}
    echo ${list_cc}
    echo ${list_buf}
    echo ${list_sch}
    echo "server -------->"
    ssh root@${SERVERIP} sysctl -w net.ipv4.tcp_congestion_control=${cc}
    ssh root@${SERVERIP} sysctl -w net.ipv4.tcp_wmem="\"${buf} ${buf} ${buf}\""
    ssh root@${SERVERIP} sysctl -w net.mptcp.mptcp_scheduler=${sch}

    echo "client -------->"
    sudo sysctl -w net.ipv4.tcp_congestion_control=${cc}
    sudo sysctl -w net.ipv4.tcp_rmem="${buf} ${buf} ${buf}"
    sudo sysctl -w net.mptcp.mptcp_scheduler=${sch}
}

# @param $1 - file name
function create_random_file
{
    src=/dev/urandom
    dst=/var/www/blocks
    
    case $1 in
	600M )
	    ssh root@${SERVERIP} dd if=${src} of=${dst}/600M.dat bs=20MB count=30
	    ;;
	* )
	    ssh root@${SERVERIP} dd if=${src} of=${dst}/${1} bs=${1%%.*}B count=1
	    ;;
    esac
}

# @param $1 - download time
function killwget
{
    sleep $1
    sudo pkill wget
} 

# @param $1 - time gap between two tests
function control_time
{
    test_date=`date "+%M"`
    clear
    echo "Waiting for Test..."
    while (( `expr $test_date % $1` != 0 ))
    do
        test_date=`date "+%M"`
    done

}

# @param $1 - train directory path
function test
{
    clear
    
    start_time=`date +%s.%N`
    end_time=0

    # file=${list_fl[ $RANDOM % ${#list_fl[@]} ]}
    # cc=${list_cc[ $RANDOM % ${#list_cc[@]} ]}
    # buf=${list_buf[ $RANDOM % ${#list_buf[@]} ]}
    # sch=${list_sch[ $RANDOM % ${#list_sch[@]} ]}
    # file=${list_fl[0]}
    # cc=${list_cc[0]}
    # buf=${list_buf[0]}
    # sch=${list_sch[0]}

    get_expr_type ${file} ${cc} ${buf} ${sch}

    echo "Prepare to start experiment #${id}"
    echo
    echo "file = ${file}"
    echo "congestion control = ${cc}"
    echo "buffer size = ${buf}"
    echo "scheduler = ${sch}"
    echo "experiment type = ${expr_type}"
    
    client_path=${1}/${id}.${start_time}
    
    mkdir -p ${client_path}
    echo ${cc}  > ${client_path}/congestion_control
    echo ${buf} > ${client_path}/buffer_size
    echo ${sch} > ${client_path}/scheduler
    echo ${expr_type} > ${client_path}/expr_type
    echo ${start_time} > ${client_path}/start_time

    server_path="/home/thu-mptcp-test/thu-mptcp-server/"
    server_pcap_path=${server_path}/server.${id}.${expr_type}.eth1.${start_time}.pcap ####???
    server_pcap_path_2=${server_path}/server.${id}.${expr_type}.eth2.${start_time}.pcap
    echo ${server_pcap_path} > ${1}/server_pcap_path
    echo ${server_pcap_path_2} >> ${1}/server_pcap_path
    echo ${SERVERIP} > ${1}/server_ip

# ==========================================================

    # create_random_file ${file}
    # control_time 5
    ssh root@${SERVERIP} tcpdump tcp -U -s 96 -i eth1 -w ${server_pcap_path} & ####???
    ssh root@${SERVERIP} tcpdump tcp -U -s 96 -i eth2 -w ${server_pcap_path_2} &

    for iface in ${list_iface[@]}; do
	# carrier=`iwconfig ${iface} | grep ESSID | cut -d':' -f2 | cut -d '"' -f2 | cut -d' ' -f1`
	iface_path=${client_path}/${iface}
	# iface_file_name=${id}.${carr_type}.${expr_type}.${carrier}.${start_time}
        iface_file_name=${id}.${expr_type}.${start_time}
	client_pcap_path=${iface_path}/client.${iface_file_name}.pcap
	throughput_path=${iface_path}/${iface_file_name}.thp

	mkdir -p ${iface_path}
	echo `ifconfig ${iface} | grep 'inet addr:' | cut -d':' -f2 | awk '{ print $1 }'` > ${iface_path}/ip_address
	# echo ${carrier} > ${iface_path}/carrier
	echo ${iface} > ${iface_path}/interface
	
	sudo tcpdump tcp -U -s 96 -i ${iface} -w ${client_pcap_path} &  #### ????
	sudo ./loop.sh -i ${iface} -o ${throughput_path} &  #### ????
	done
	
	if [ -e ${file}".dat" ]; then
		rm  ${file}".dat"
	fi
	
    
    python static_ixia.py ${1} ${2} ${3} ${4} ${id} & # start the python  
    countdown 15 "download"

	start_size_eth1=`cat /sys/class/net/eth1/statistics/rx_bytes`
    start_size_eth2=`cat /sys/class/net/eth2/statistics/rx_bytes`
    
	killwget 100&
    wget ${SERVERIP}/blocks/${file}".dat"
    du -b ${file}".dat" | cut -f1 > ${client_path}/download_size
    download_size_sum=`du -b ${file}".dat" | cut -f1`
    
	rm ${file}".dat"
    
	ps -ef|grep static_ixia.py|grep -v grep|cut -c 9-15|xargs kill -9 # kill python process
    
	end_time=`date +%s.%N`
    echo ${end_time} > ${client_path}/end_time

    ssh root@${SERVERIP} pkill tcpdump
    sudo pkill tcpdump
    sudo pkill loop.sh
    end_size_eh1=`cat /sys/class/net/eth1/statistics/rx_bytes`
    end_size_eh2=`cat /sys/class/net/eth2/statistics/rx_bytes`
    for iface in ${list_iface[@]}; do
	# carrier=`cat ${client_path}/${iface}/carrier`
	iface_path=${client_path}/${iface}
	# iface_file_name=${id}.${carr_type}.${expr_type}.${carrier}.${start_time}
    iface_file_name=${id}.${expr_type}.${start_time}
	
	client_pcap_path=${iface_path}/client.${iface_file_name}.pcap
	throughput_path=${iface_path}/client.${iface_file_name}.thp
    ip_address=`ifconfig ${iface} | grep 'inet addr:' | cut -d':' -f2 | awk '{ print $1 }'`
     receive_size_eh1=$((${end_size_eh1}-${start_size_eth1}))
    receive_size_eh2=$((${end_size_eh2}-${start_size_eth2}))
     echo ${id} ${expr_type} ${start_time} ${end_time} ${download_size_sum} ${receive_size_eh1} ${receive_size_eh2} ${file} ${cc} ${buf} ${sch} ${iface} ${ip_address} ${client_pcap_path} ${throughput_path} ${server_pcap_path} ${server_pcap_path_2} >> ${1}/global.log  # ${carrier}

    done
    (( id++ ))
    echo ${end_time} > ${1}/train_end_time
}

function finish
{
    ssh root@${SERVERIP} pkill tcpdump
    sudo pkill tcpdump
    sudo pkill loop.sh

    if [[ -n "`pgrep wget`" ]]; then
	for iface in ${list_iface[@]}; do
	    # carrier=`cat ${client_path}/${iface}/carrier`
	    iface_path=${client_path}/${iface}
	    # iface_file_name=${id}.${carr_type}.${expr_type}.${iface}.${start_time}
            iface_file_name=${id}.${expr_type}.${iface}.${start_time}
	    client_pcap_path=${iface_path}/client.${iface_file_name}.pcap
	    throughput_path=${iface_path}/client.${iface_file_name}.thp
	    ip_address=`ifconfig ${iface} | grep 'inet addr:' | cut -d':' -f2 | awk '{ print $1 }'`
	    echo ${id} ${expr_type} ${start_time} ${end_time} ${file} ${cc} ${buf} ${sch} ${iface} ${ip_address}  ${client_pcap_path} ${throughput_path} ${server_pcap_path}  >> ${1}/global.log
            # ${carrier} ${carr_type}
	done
    fi

    exit
}

#--------------------------------------------------------------------------------------------------------------------------


#trap finish SIGINT

if [[ -z $1 ]]; then
    echo "Please input current HSR ID and try again"
    exit
fi
if [[ -z $2 ]]; then
    echo "Please input ethernetDelay type and try again"
    exit
fi
if [[ -z $3 ]]; then
    echo "Please input packetDrop type and try again"
    exit
fi
if [[ -z $4 ]]; then
    echo "Please input bitRate type and try again"
    exit
fi
# sudo ntpdate time-a.nist.gov


python json_reset.py
get_iface_and_carrier
while : ; 
do
    # control_time 5
	countdown 5 "next test"	
	load_env ${root_dir} "${1}"	
	#python static_ixia.py ${root_dir}/${1} ${2} ${3} ${4} ${id} # start the python 
	test ${root_dir}/${1} ${2} ${3} ${4}
    python json_reset.py
done

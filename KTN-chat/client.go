package main

import(
	"net"
	"encoding/json"
	"fmt"
	"time"
)
const (
	RECV_BUF_LEN = 1024
)
const (
	login 		= "login"
	message 	= "message"
	logout 		= "logout"
	response 	= "response"
	error		= "error"
	username	= "username"
	messages 	= "messages"
	request 	= "request"
)

func main()(){
	 //map[string]string{"request": "login","username":"ciffen"}
	serverAddr, _ := net.ResolveTCPAddr("tcp", "192.168.1.4:9999")
	con, _ := net.DialTCP("tcp", nil, serverAddr);
	buf := make([]byte, RECV_BUF_LEN)
	var fromUser string
	for {
		msg := make(map[string]interface{})
		go func(){
			var msgIn  map[string] interface{}
			buf2 := make([]byte, RECV_BUF_LEN)
			rlen,err := con.Read(buf2)
			if err != nil {
				fmt.Printf("Error: %v", err)
	        }
			json.Unmarshal(buf2[:rlen],&msgIn)
			for k, v:= range msgIn{
				fmt.Printf("key:%s, val: %s \n",k,v)
			}
		}()
		time.Sleep(time.Millisecond*100)
		fmt.Printf("Request: ")
		_,err:=fmt.Scanf("%s\n",&fromUser)
		if err != nil {
			fmt.Printf("Error: %v", err)
		}
		msg[request]=fromUser
		if fromUser == login{
			fmt.Printf("Username: ")
			_,err:=fmt.Scanf("%s\n",&fromUser)
			if err != nil {
				fmt.Printf("Error: %v", err)
			}
			msg[username]=fromUser
		} else if fromUser == logout{
		} else{
			fmt.Printf("Message: ")
			_,err=fmt.Scanf("%s\n",&fromUser)
			if err != nil {
				fmt.Printf("Error: %v", err)
			}
			msg[message]=fromUser
		}
		buf,err =json.Marshal(msg)
		if err!=nil {
			fmt.Printf("Error: %v", err)
		}
		//fmt.Printf("%d", msg)
		con.Write(buf)
	}
}

package main

import(
	"net"
	"encoding/json"
	"fmt"
	"time"
	"os"
	"log"
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
	serverAddr, _ := net.ResolveTCPAddr("tcp", "192.168.1.4:9999")
	con, err := net.DialTCP("tcp", nil, serverAddr);
	fmt.Printf("Connected to server. \n")
	if err != nil{
		log.Printf("Error: %v",err)
		os.Exit(1)
	}
	buf := make([]byte, RECV_BUF_LEN)
	fmt.Printf("Welcome, good sir, to the Chat of Awesomeness!\n")
	fmt.Printf("Type a message and hit Enter to send (Type 'login' to log in; type 'logout' to log out.) \n")
	go func(){
		for {
			var msgIn  map[string] interface{}
			buf2 := make([]byte, RECV_BUF_LEN)
			rlen,err := con.Read(buf2)
			if err != nil {
				fmt.Printf("Error: %v", err)
	        }
			err =json.Unmarshal(buf2[:rlen],&msgIn)
			if err != nil{
				log.Printf("Error: %v",err)
			}
			printToScreen(msgIn)
		}
	}()
	for {
		time.Sleep(time.Millisecond*100)
		msg := getInputFromUser()
		buf,err =json.Marshal(msg)
		if err!=nil {
			fmt.Printf("Error: %v", err)
		}
		con.Write(buf)

	}
}
func getInputFromUser() (msg map[string]string){
	var fromUser string
	fmt.Printf(": ")
	_,err:=fmt.Scanf("%s\n",&fromUser)
	if err != nil {
		fmt.Printf("Error: %v", err)
	}
	
	msg =make(map[string]string)
	msg[request]=message
	switch fromUser {
		case login:
			msg[request]=login
			fmt.Printf("Username: ")
			_,err:=fmt.Scanf("%s\n",&fromUser)
			if err != nil {
				fmt.Printf("Error: %v", err)
			}
			msg[username]=fromUser
			return 
		case logout:
			msg[request]=logout
		default:
			msg[message]=fromUser	
	}
	return
}
	
func printToScreen(msgIn map[string] interface{}){
	if resp, ok:= msgIn[response]; ok{
		switch resp{
			case login:
				if un, unPres := msgIn[username]; unPres{
					if errMsg, unErr := msgIn[error]; unErr{
						fmt.Printf("Username: %s - %s \n", un, errMsg)
					} else {
						fmt.Printf("Your are logged in with username: %s \n", un)
						if messages, msgsOk := msgIn[messages]; msgsOk{
							fmt.Printf("Previous messages:\n %s",messages)
						}
					}
				}
			case message:
				if err, msgErr := msgIn[error]; msgErr{
					fmt.Printf("%s \n", err)
				} else if msg, msgOk := msgIn[message]; msgOk{
					fmt.Printf("%s \n", msg)
				}
			case logout:
				if un, unPres := msgIn[username]; unPres{
					if err, lgoErr := msgIn[error]; lgoErr{
						fmt.Printf("User:%s %s \n", un, err)
					} else{
						fmt.Printf("User: %s has logged out. \n", un)
					}
				}
		}
	}
}
					
					
			
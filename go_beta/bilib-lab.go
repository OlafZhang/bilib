package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
	"regexp"
)


// 正则表达式法匹配(暂时觉得json很麻烦)

func main() {
	resp, err := http.Get("https://api.bilibili.com/x/web-interface/view?aid=114514")
	if err != nil {
    	fmt.Println("Hello world")
	}
	defer resp.Body.Close()  // 函数结束时关闭Body
	body, err := ioutil.ReadAll(resp.Body)  // 读取Body
	fmt.Println(string(body))

	reg1 := regexp.MustCompile(`"name":".+?"`)
    if reg1 == nil { //解释失败，返回nil
        fmt.Println("regexp err")
        return
    }
    //根据规则提取关键信息
	result1 := reg1.FindAllStringSubmatch(string(body), -1)
	fmt.Println("result1 = ", result1)
}




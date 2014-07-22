#include <string>
#include <iostream>
#include <fstream>
#include <pqxx/pqxx>
#include <curl/curl.h>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
//when we open our ofstream, we should write a representation of our SID to the damn thing.

using namespace rapidjson;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp){
  ((std::string*)userp)->append((char*)contents, size * nmemb);
  return size * nmemb;
}

//return 0 on success, d 
//return 1 on error, 
//pass an unallocated pointer to the thing.
int openSafely(std::string *url, Document d, int segment, std::ofstream errLog){
  CURL *curl;
  CURLcode res;
  std::string *read_buffer = NULL;
  //this init might burst into flames if we are using threads.
  //otherwise, read_buffer should contain our string afterwards
  curl = curl_easy_init();
  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url->c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, read_buffer);
    res = curl_easy_perform(curl);
    if(res!=CURLE_OK){
      errLog << "curl performance error " << res << ", at segment " << segment << std::endl;
    }
    curl_easy_cleanup(curl);
  }else{
    errLog << "curl init error " << curl << ", at segment " << segment << std::endl;
    return 1;
  }

  d.Parse<0>(read_buffer->c_str());
  std::cout << *read_buffer << std::endl;
  return 0;
}

int crawlUser(){
  std::ofstream errLog;
  errLog.open("output.txt", std::ofstream::out | std::ofstream::app);
  std::string apiKey = "IkJtqSbg6Nd3OBnUdaGl9YWE3ocupygJcnPebHRou8eFbd4RUv";
  std::string username = "dduane";
  std::string blogString = string("http://api.tumblr.com/v2/blog/") + username + string(".tumblr.com/info?api_key=")  + apiKey;
  std::string postString = string("http://api.tumblr.com/v2/blog/") + username + string(".tumblr.com/posts?api_key=") + apiKey;
  std::string noteString = string("http://api.tumblr.com/v2/blog/") + username + string(".tumblr.com/likes?api_key=") + apiKey;
  Document response;

  /*user section
    expect this to add a user field to the database.
   */
  if (1 == openSafely(blogString, response, 0, errLog)){
    return 1;
  }
  int likeCount = 0;
  std::string blogURL = response['response']['blog']['url'];
  std::string username = response['response']['blog']['title'];
  std::string updated = response['response']['blog']['updated'];
  std::string postCount = response['response']['blog']['posts'];
  if(response['response']['blog']['share_likes']){
    likeCount = response['response']['blog']['share_likes'];
  }else{
    likeCount = -1
  }
  errLog << "wrote all the record";
  return 0;
}

int main(int argc, char **argv){
  int id = argv[1];//get a process id of some sort
  bool debug = 1;
  int ret = crawlUser();
  return 0;
}



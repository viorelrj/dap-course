# Seminar 3

[This](https://levelup.gitconnected.com/comparing-api-architectural-styles-soap-vs-rest-vs-graphql-vs-rpc-84a3720adefa) paper focuses on explaining and comparingdifferent aspects of service communication API's

First it describes rpc, how it is pretty close to the hardware and offers stubs, which act as a software layer  which takes care of mesage encoding and decoding. These are usually generated from the content of a .proto file describing the interface and can be imported as libraries for the services that need to communicate, in a client-server manner.

Also it introduces SOAP, which has its messages usually written in xml, which can get really heavy-weight, but the messages are very extensible and can facilitate web service security. This comes to be the go-to option for applications with strict security policies.

The REST is the most common nowadays - communication through JSON to represent a part of the application state, although there are quite a few implemntations that use TRUE REST, but rather a dumbed-down rpc over HTTP. The true implementation HATEOAS (Hypermedia as the Engine of Application State) allows the client to have little to no context on how to interact with the server, so that the client gets decoupled from the server as much as possible.

REST is usually the go-to sollution for communicating, but in case where the database has complex relations and the requests structures might vary in a great way, it becomes cumbersome to write endpoints for each model and responses come to be bloated with useless data, thus facebook came out with GraphQL, which requires the developers to carefuly describe all the relations once and allow the API to select only the needed data. I tend to oversimplify it and call it "sql for frontend devs".
One additional feature the GraphQl has is that it supports subscriptions, which allow the clients to be notified about new events, like push notifications.


If to order the API's by message size, it would be:
RPC,
GraphQl,
REST,
SOAP

And as described in documentation, rpc seems to be quite nice for internal communication between services, because the discoverability (which is a major flaw in rpc) is not that problematic in this context; And it allows fast messaging because the size is quite small and decoding is quite fast. So I use them for workers.

The "frontend" of the system should be sufficient with a simple REST api, as the requests aren't too troublesome, the communication being reduced to string request for a string array response, maintaining the optimal speed without any engineering overhead.
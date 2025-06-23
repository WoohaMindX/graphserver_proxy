"use client"

import { useStream } from "@langchain/langgraph-sdk/react"
import type { Message } from "@langchain/langgraph-sdk"

export function Assistant() {
    const thread = useStream<{ messages: Message[] }>({
        apiUrl: process.env["NEXT_PUBLIC_LANGGRAPH_API_URL"] ?? "",
        assistantId: process.env["NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID"] ?? "",
        messagesKey: "messages",
        onUpdateEvent: (event: any) => {
            console.log("Update event:", event);
        },
    });

    return (
        <div>
            <div>
                { thread.messages.map((message) => (
                    <div key={message.id}>
                        <div>{message.id as string}:</div>
                        <div>{message.content as string}</div>
                    </div>
                ))}
            </div>


            <form onSubmit={(e) => {
                e.preventDefault();
                const form = e.target as HTMLFormElement;
                const message = new FormData(form).get("message") as string;

                form.reset();
                thread.submit({ messages: [{"type": "human", "content": message}] });
            }}>
                <input 
                    type="text" 
                    name="message" 
                    style={{
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        padding: '8px 12px',
                        fontSize: '14px',
                        outline: 'none',
                        transition: 'border-color 0.2s',
                    }}
                    onFocus={(e) => e.target.style.borderColor = '#007bff'}
                    onBlur={(e) => e.target.style.borderColor = '#ccc'}
                />
                {thread.isLoading ? (
                    <button key="stop" type="button" onClick={() => thread.stop()} style={{
                        marginLeft: '8px',
                        padding: '8px 12px',
                        backgroundColor: '#f0f0f0',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                    }}>
                        Stop
                    </button>
                ) : (
                    <button type="submit" style={{
                        marginLeft: '8px',
                        padding: '8px 12px',
                        backgroundColor: '#007bff',
                        border: 'none',
                        borderRadius: '4px',
                        color: '#fff',
                        cursor: 'pointer',
                    }}>
                        Send
                    </button>
                )}
            </form>

        </div>


    )


}
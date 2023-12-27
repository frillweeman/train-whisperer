<script>
  import { onMount, onDestroy } from "svelte";
  import VirtualList from "$lib/global-components/VirtualList.svelte";

  export let messages = [];
  export let channelNames = [""];

</script>

<div class="chat-container overflow-auto pt-3 px-4">
  <VirtualList items={messages} let:item autoScroll>
    <div
      class="chat chat-start my-2"
      class:text-left={item.channelIndex === 1}
      class:text-right={item.channelIndex === 2}
    >
      <div class="chat-bubble mb-0">{item.text}</div>
      <div class="chat-footer mt-0">
        <span class="text-xs font-bold">{channelNames[item.channelIndex - 1] ?? "Broadcast"}</span>
        <time class="text-xs opacity-50">{new Date(item.timestamp).toLocaleTimeString([], {
          timeStyle: "short",
        })}</time>
      </div>
    </div>
  </VirtualList>
</div>

<style>
/* .chat-container {
  height: calc(100vh - 208px);
} */

.chat-container {
  height: calc(100vh - 208px);
  position: relative;
}

.chat-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px; /* Adjust this value to control the height of the gradient */
  background: linear-gradient(to bottom, rgba(36, 44, 70, 0), rgba(36, 44, 70, 1));
  pointer-events: none; /* This allows the user to still interact with the content underneath the gradient */
}
</style>

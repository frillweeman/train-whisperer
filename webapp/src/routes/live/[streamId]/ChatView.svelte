<script>
  import { onMount, onDestroy } from "svelte";

  export let messages = [];
  export let channelNames = [""];

  let scrollableContainer;
  let scrollSmooth = false;

  function scrollToBottom() {
    scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
  };

  function onNewMessage() {
    const isCloseToEnd = scrollableContainer.scrollHeight - scrollableContainer.scrollTop - scrollableContainer.clientHeight < 100;
    if (isCloseToEnd) {
      console.log("attempting to scroll to the bottom");
      scrollToBottom();
    } else {
      console.log("not scrolling to the bottom");
    }
  }

  onMount(() => {
    scrollToBottom(); // jump to bottom on first load
    scrollSmooth = true; // smoothly scroll to bottom on new messages
  });

</script>

<div bind:this={scrollableContainer} class="chat-container overflow-auto pt-3 px-4" class:scroll-smooth={scrollSmooth}>
  {#each messages as message}
    <div class="chat chat-start my-2">
      <!-- <div class="chat-header">
        <span class="mx-2 text-xs">{channelNames[message.channel]}</span>
      </div> -->
      <div class="chat-bubble mb-0">{message.text}</div>
      <div class="chat-footer mt-0">
        <time class="text-xs opacity-50">{new Date(message.time).toLocaleTimeString([], {
          timeStyle: "short",
        })}</time>
      </div>
    </div>
  {/each}

  <hr class="my-4" />
</div>

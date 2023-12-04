<script>
  import Button from "$lib/global-components/Button.svelte";
  import ChatView from "./ChatView.svelte";

  export let data;

  $: activeStream = data.streams.find(stream => stream.active);
</script>

<div>
  {#if activeStream}
    <div>
      <h2 class="text-lg font-bold text-center">{activeStream.title}</h2>

      <ChatView messages={data.transcriptions[`${activeStream.id}`]} channelNames={activeStream.channelNames} />

      <div class="mt-2 flex justify-end">
        <!-- TODO: make a play/stop button and keep this hidden -->
        <audio controls>
          <source src={activeStream.url} type="audio/mpeg" />
        </audio>
        <Button ghost>
          <svg class="h-6 fill-black dark:fill-slate-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>stop</title><path d="M18,18H6V6H18V18Z" /></svg>
          <span>Stop Monitoring</span>
        </Button>
      </div>
    </div>
  {:else}
    <div>No active streams</div>
  {/if}
</div>

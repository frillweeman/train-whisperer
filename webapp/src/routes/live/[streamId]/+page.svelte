<script lang="ts">
  import ChatView from "./ChatView.svelte";
  import { popup } from "@skeletonlabs/skeleton";
  import type { PopupSettings } from "@skeletonlabs/skeleton";
  import { streams, activeStream, setActiveStream, deactivateStream, renameChannels } from "../../../stores/streams";
  import { page } from "$app/stores";
  import { onMount, onDestroy } from "svelte";
  // import { BrowserTranscription, BrowserStream } from "../../../lib/types";

  let eventSource: EventSource | undefined = undefined;
  let transcriptions: any[] = [];
  let eventSourceRetryTimeout = 1000;
  let audioElement: HTMLAudioElement | undefined = undefined;

  $: currentStream = $streams.find(stream => stream._id === $page.params.streamId);
  $: isActive = (currentStream !== undefined) && (currentStream?._id === $activeStream?._id);
  $: if (isActive || currentStream) {
    startMonitoring();
  }

  const popupConfirmMonitoring: PopupSettings = {
    event: 'click',
    target: 'confirmMonitoring',
    placement: 'bottom',
  };

  const popupConfirmClear: PopupSettings = {
    event: 'click',
    target: 'confirmClear',
    placement: 'bottom',
  };

  let isMuted = true;

  function toggleAudioStream(): void {
    isMuted = !isMuted;
    if (!audioElement) {
      return;
    }
    if (isMuted) {
      audioElement.pause();
    } else {
      audioElement.src = null;
      audioElement.src = currentStream.url;
      audioElement.play();
    }
  }

  function stopMonitoring(): void {
    eventSource?.close();
    deactivateStream();
  }

  async function startMonitoring() {
    if (!($streams.length && currentStream)) {
      return;
    }

    eventSource?.close();

    transcriptions = await fetch(`/api/transcriptions/${currentStream._id}`).then(res => res.json());

    if (isActive) {
      // TODO: make this a config val
      const sseUrl = (import.meta as any).env.VITE_IS_DOCKER ? 
        'https://youthfulgoon.com/sse' :
        'http://localhost:8000/transcriptions/live';
      eventSource = new EventSource(sseUrl);

      eventSource.onmessage = (event) => {
        const newTranscription: any = JSON.parse(event.data);
        transcriptions = [...transcriptions, newTranscription];
      }

      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
        setTimeout(startMonitoring, eventSourceRetryTimeout);
        if (eventSourceRetryTimeout < 30000) // max 30 seconds
          eventSourceRetryTimeout *= 2; // Double the timeout for the next retry
      }
    } else {
      console.debug(`id ${currentStream._id} not active (${$activeStream?._id}), not starting EventSource`);
    }
  }

  function clearTranscriptions(): void {
    fetch(`/api/transcriptions/${currentStream._id}`, { method: 'DELETE' })
      .then(() => {
        transcriptions = [];
      })
      .catch(err => console.error(err));
  }

  // TODO: type this correctly
  function handleChannelRename({ detail }: any): void {
    const { channelNumber, newChannelName } = detail;
    const channel1 = channelNumber === 1 ? newChannelName : (currentStream.channelNames[0] ?? "Broadcast");
    const channel2 = channelNumber === 2 ? newChannelName : (currentStream.channelNames[1] ?? "Broadcast");
    const newChannelNames = [channel1, channel2];
    renameChannels(currentStream._id, newChannelNames);
  }

  onDestroy(() => {
    eventSource?.close();
  });
</script>

<div>
  {#if currentStream}
  <div>

    <div class="p-2 sticky left-0 top-0 w-full flex justify-between bg-surface-700 z-10">
      <div>
        <a class="btn-icon" href="/live">
          <i class="fas fa-chevron-left" />
        </a>
        <button use:popup={popupConfirmMonitoring} class="btn-icon hover:variant-soft-primary">
          {#if isActive}
            <i class="fas fa-circle text-green-500 text-lg pulse" />
          {:else}
            <i class="fas fa-circle text-red-500 text-lg" />
          {/if}
        </button>
      </div>

      <!-- Confirm Popup -->
      <div class="card p-4 w-72 shadow-xl variant-filled-surface" data-popup="confirmMonitoring">
        <div>
          {#if isActive}
            <p>Are you sure you want to stop monitoring?</p>
            <button on:click={stopMonitoring} class="mt-3 btn w-full variant-filled-error"><i class="fas fa-stop mr-2" />STOP</button>
            {:else}
            <p>Are you sure you want to start monitoring? Transcribing can be expensive if run for long periods.</p>
            <button on:click={setActiveStream.bind(null, currentStream._id)} class="mt-3 btn w-full variant-filled"><i class="fas fa-play mr-2" />START</button>
          {/if}
        </div>
        <div class="arrow variant-filled-surface" />
      </div>
                

      <div class="flex items-center max-w-sm truncate">
        <span class="h4 font-bold">{currentStream.title}</span>
      </div>
      
      <div>
        <button class="btn-icon hover:variant-soft-primary" use:popup={popupConfirmClear}>
          <i class="fas fa-ban" />
        </button>
        <button on:click={toggleAudioStream} class="btn-icon hover:variant-soft-primary">
          {#if isMuted}
            <i class="fas fa-volume-mute text-lg" />
          {:else}
            <i class="fas fa-volume-high text-lg" />
          {/if}
        </button>

        <!-- Confirm Popup -->
        <div class="card p-4 w-72 shadow-xl variant-filled-surface" data-popup="confirmClear">
          <div>
              <p>Are you sure you want to clear the transcript? This can't be undone.</p>
              <button on:click={clearTranscriptions} class="mt-3 btn w-full variant-filled-error"><i class="fas fa-ban mr-2" />CLEAR</button>
          </div>
          <div class="arrow variant-filled-surface" />
        </div>
      </div>
    </div>

    {#if transcriptions.length > 0}
      <ChatView on:renameChannel={handleChannelRename} messages={transcriptions} channelNames={currentStream.channelNames} />
    {:else}
      <div class="text-center h4 p-4">Nothing yet!</div>
    {/if}

    <audio bind:this={audioElement} class="hidden" src={null} />      
  </div>
  {/if}
</div>

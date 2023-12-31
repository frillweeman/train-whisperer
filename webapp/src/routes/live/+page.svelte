<script>
  import { activeStream } from "../../stores/streams";
  import StreamList from "./StreamList.svelte";
</script>

<svelte:head>
  <title>Live Streams | Train Whisperer</title>
</svelte:head>
<div class="p-4">
  {#if $activeStream}
    <div class="card shadow-xl mb-4">
      <header class="card-header h3 font-bold mb-6">
        <i class="fas fa-circle text-green-500 text-lg mr-2 pulse"/>
        Active Stream
      </header>
    
      <section class="px-4">
        <ul class="divide-y divide-slate-500">
          <li class="py-4 flex justify-between items-center">
            <h3>{$activeStream.title}</h3>
            <a href={`/live/${$activeStream._id}`} class="btn btn-icon variant-filled-primary">
              <i class="fas fa-play text-lg" />
            </a>
          </li>
        </ul>
      </section>
    </div>
  {/if}

  <StreamList />
</div>

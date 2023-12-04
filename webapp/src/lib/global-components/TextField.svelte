<script>
  import { createEventDispatcher } from "svelte";

  export let label = "";
  export let placeholder = "";
  export let hint = "";
  export let value = "";
  export let required = false;
  export let disabled = false;
  export let error = "";
  export let bordered = false;
  export let validationRegex = null;
  export let joined = false;

  const dispatch = createEventDispatcher();

  function handleInput(event) {
    const { value } = event.target;
    const isValid = !value || (validationRegex ? validationRegex.test(value) : true);
    error = isValid ? "" : "Invalid value";
    
    // Bubble the input event
    dispatch("input", value);
  }
</script>

<div class="w-full">
  {#if label}
    <div class="label">
      <span class="label-text">{label}</span>
    </div>
  {/if}
  <input
    on:input={handleInput}
    bind:value={value}
    type="text"
    {placeholder}
    {disabled}
    {required}
    class="input w-full"
    class:input-error={error}
    class:input-bordered={bordered}
    class:join-item={joined}
  />
  {#if error || hint}
    <div class="label">
      <span class:opacity-60={!error} class:text-error={error} class="label-text-alt">{@html (error || hint)}</span>
    </div>
  {/if}
</div>

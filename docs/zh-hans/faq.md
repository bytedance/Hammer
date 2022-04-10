# 常见问题

1. Exit with `RuntimeError: Address already in use`

    The error context may look like:

    ```shell
    Traceback (most recent call last):
      File "ddp.py", line 103, in <module>
        torch.distributed.init_process_group(backend='nccl')
      File "/usr/local/lib/python3.7/dist-packages/torch/distributed/distributed_c10d.py", line 393, in init_process_group
        store, rank, world_size = next(rendezvous_iterator)
      File "/usr/local/lib/python3.7/dist-packages/torch/distributed/rendezvous.py", line 172, in _env_rendezvous_handler
        store = TCPStore(master_addr, master_port, world_size, start_daemon, timeout)
    RuntimeError: Address already in use
    ```

    It is caused by the TCP port used for distributed training is occupied by another process.

    If you are sure this is the dedicated TCP port for you and your project, you can
    ```shell
    lsof -i:<THE_TCP_PORT_YOU_USE>
    ```
    to find the corresponding process and kill it manually.

   ---

2. Exit with `Working directory has already existed`

    The error context may look like:

    ```shell
    Working directory `work_dirs/stylegan2ada_ffhq256` has already existed!
    Please use another job name, or otherwise the results and logs may be mixed up.
    Killing subprocess 16666
    Killing subprocess 16667
    Killing subprocess 16668
    Killing subprocess 16669
    Killing subprocess 16670
    Killing subprocess 16671
    Killing subprocess 16672
    Killing subprocess 16673
    Traceback (most recent call last):
      File "/usr/lib/python3.7/runpy.py", line 193, in _run_module_as_main
        "__main__", mod_spec)
      File "/usr/lib/python3.7/runpy.py", line 85, in _run_code
        exec(code, run_globals)
      File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 340, in <module>
        main()
      File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 326, in main
        sigkill_handler(signal.SIGTERM, None)  # not coming back
      File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 301, in sigkill_handler
        raise subprocess.CalledProcessError(returncode=last_return_code, cmd=cmd)
    ```

   **This is an expected behavior of Hammer.**

   Whenever you launch a job, Hammer will create a working directory to store intermedia.

   Such a working directory is identified by your `job_name` and it is supposed to be unique.

   Hammer will prevent you from mistakenly overriding previous experiments.

   Hence, if you intend to launch several jobs, make sure to given them different identifier by passing `--job_name <A_UNIQUE_NAME>`.

   ---

3. Get stuck right after running `dist_train.sh`

   This may because of different TCP ports are assigned to each replica for communication.

   If it is, manually assign a free port via `PORT=<AN_AVAILABLE_PORT>` when executing `dist_train.sh`.

   ---

4. Get stuck at the log `Start training...`

   The most possible reason is some `lock` files may block the training.

   These `lock` files are probably result from previous accidentally aborted job, especially when interrupt during CUDA kernel compiling.

   To verify, list all files via:

   ```shell
   la $HOME/.cache/torch_extensions/<EXTENSION_NAME>
   ```

   If there's a folder named `lock`, delete it.

   ---

5. Run Bash script but fail with `/bin/bash^M: bad interpreter: No such file or directory`

   Please refer to [this discussion](https://askubuntu.com/questions/304999/not-able-to-execute-a-sh-file-bin-bashm-bad-interpreter).

   This is because the line endings of this script file is accidentally changed from Unix style to DOS/Windows style.

   Check if you've configured any auto-formatting tools that changed `LF` to `CRLF` in your editor like VS Code.

   You can also change such a file back via:

   ```shell
   sed -i -e 's/\r$//' <YOUR_SCRIPT>
   ```

   ---

6. Exit with `` when building `train` data loader

   The error context may look like:

   ```shell
   Traceback (most recent call last):
     File "/usr/lib/python3.7/runpy.py", line 193, in _run_module_as_main
      "main", mod_spec)
     File "/usr/lib/python3.7/runpy.py", line 85, in _run_code
      exec(code, run_globals)
     File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 340, in <module>
      main()
     File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 326, in main
      sigkill_handler(signal.SIGTERM, None) # not coming back
     File "/usr/local/lib/python3.7/dist-packages/torch/distributed/launch.py", line 301, in sigkill_handler
      raise subprocess.CalledProcessError(returncode=last_return_code, cmd=cmd)
   ```

   This **may** because of running out of CPU memory.

   You can have a try on following approaches:

      - Prepare a machine with larger memory.
      - Decrease `data_repeat`.
      - Set `data_pin_memory=false` (may cause slow).
      - Install `jemalloc`.
      - Decrease `train_max_samples` and `val_max_samples` (may cause inferior performance).

   ---

If content above cannot help you, feel free to leave an issue [here](https://github.com/bytedance/Hammer/issues).
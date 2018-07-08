import argparse
import json

import mlpipe.mlpipeutils as mlpipeutils
import yaml


class BuildinJob:
    def _get_loop_parameters(self, loop_param):
        if (len(loop_param) == 0):
            return
        if (len(loop_param) == 1):
            k, k_list = loop_param[0]
            for v in k_list:
                yield {k: v}
        else:
            k, k_list = loop_param[0]
            for w in self._get_loop_parameters(loop_param[1:]):
                for v in k_list:
                    z = w.copy()
                    z.update({k: v})
                    yield z

    def _loop_search(self, pipe, loop_job_name, loop_job_conf):
        loop_param = []
        for k in loop_job_conf['parameters']['loop_parameters']:
            k_list = eval(loop_job_conf['parameters']['loop_parameters'][k])
            loop_param.append((k, k_list))
        templ = loop_job_conf['parameters']['template']
        templ_str = json.dumps(templ)
        self.all_job_hash = []
        # iterate all possible param combination
        for pm in self._get_loop_parameters(loop_param):
            job_conf_str = templ_str % pm
            job_conf = yaml.safe_load(job_conf_str)
            job_h = durianutils.get_md5(json.dumps(job_conf))
            new_job_name = loop_job_name + "_" + job_h
            self.all_job_hash.append(job_h)
            print(job_conf)
            for ko in job_conf["output"].keys():
                job_conf["output"][ko] += "_" + job_h
            pipe['jobs'][new_job_name] = job_conf
        # create an aggregating job
        agg_job = {}
        agg_job_name = loop_job_name + "_loop_search_agg_min"
        search_result_file = pipe['jobs'][loop_job_name]['parameters']['search_result_file']
        agg_job["input"] = {}
        for ip in templ["output"]:
            agg_job["input"][ip] = [templ["output"][ip] + "_" + j_h for j_h in self.all_job_hash]
        agg_job["output"] = templ["output"]
        agg_job["parameters"] = loop_job_conf["parameters"]
        agg_job["module"] = "mlpipe/module/find_min"
        pipe["jobs"][agg_job_name] = agg_job

    def compile_pipe(self, pipe):
        durian_jobs = [j for j in pipe['jobs'] if "/" not in pipe['jobs'][j]['module']]
        for lj in durian_jobs:
            j_c = pipe['jobs'][lj]
            if j_c['module'] == "loop_search":
                self._loop_search(pipe, lj, j_c)
                pipe['jobs'].pop(lj, None)
        return pipe


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pipe_file', help='original pipe file name')
    parser.add_argument('compiled_file', help='output pipe file name')

    params = parser.parse_args()
    with open(params.pipe_file, "r") as yf:
        pipe = yaml.load(yf)
        lbin = DurianBuildinJob()
        compiled_pipe = lbin.compile_pipe(pipe)
        with open(params.compiled_file, "w") as fo:
            yaml.dump(compiled_pipe, fo, default_flow_style=False)

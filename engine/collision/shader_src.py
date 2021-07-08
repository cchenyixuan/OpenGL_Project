vertex_src = """
# version 440 core
layout(location=0) in vec3 pos;
layout(location=1) in vec2 tex;
layout(location=2) in vec3 nor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 offset;
uniform int is_static;
out vec2 f_tex;
out vec3 f_nor;
void main(){
    switch(is_static){
        case 0:
            gl_Position = projection * view * model * vec4(pos, 1.0);
            break;
        case 1:
            gl_Position = projection * view * model * vec4(pos, 1.0);
            break;
    }
    f_tex = tex;
    f_nor = nor;
}
"""
fragment_src = """
# version 440 core
in vec2 f_tex;
in vec3 f_nor;
out vec4 color;
uniform sampler2D texture_2d;
uniform int mode;
void main(){
    switch(mode){
        case 0:
            color = texture(texture_2d, f_tex);//vec4(0.0, 1.0, 0.0, 1.0);
            break;
        case 1:
            color = vec4(1.0, 1.0, 0.0, 1.0);
            break;
        case 2:
            color = texture(texture_2d, f_tex);//vec4(1.0, 0.0, 0.0, 1.0);
            break;

    }


}
"""
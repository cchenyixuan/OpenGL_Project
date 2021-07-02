vertex_src = """
# version 330 core
layout(location=0) in vec4 vertex;
layout(location=1) in vec2 instance_offset;

out vec2 TexCoords;
out vec4 ParticleColor;

uniform mat4 projection;
uniform vec4 color;
uniform vec3 offset[1000];

void main(){
    float scale = 2.0f;
    TexCoords = vertex.zw;
    ParticleColor = vec4(color.xyz, offset[gl_InstanceID].z);
    gl_Position = projection * vec4((vertex.xy*scale)+offset[gl_InstanceID].xy, 0.0, 1.0);
}


"""


fragment_src = """
# version 330 core
in vec2 TexCoords;
in vec4 ParticleColor;

out vec4 color;

uniform sampler2D sprite;

void main(){
    color = (texture(sprite, TexCoords) * ParticleColor);
}

"""

